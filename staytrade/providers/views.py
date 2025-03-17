from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
    TemplateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy
from staytrade.providers.models import Hotel, RoomType
from staytrade.providers.forms import (
    HotelBasicInfoForm,
    HotelLocationForm,
    HotelImagesForm,
    RoomTypeBasicInfoForm,
    RoomTypeCapacityForm,
    RoomTypeImagesForm,
)
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


# Main area
class MyAreaView(LoginRequiredMixin, TemplateView):
    template_name = "providers/providers_area.html"


# Hotel related views
class HotelDetailView(LoginRequiredMixin, DetailView):
    model = Hotel
    template_name = "providers/hotel_detail.html"
    context_object_name = "hotel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

    # Protects form outter users to view details.
    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)


class MyHotelsListView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = "providers/hotels_list.html"
    context_object_name = "hotels"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user).order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Hotel list.")
        return context


class HotelDeleteView(LoginRequiredMixin, DeleteView):
    model = Hotel
    success_url = reverse_lazy("providers:my_hotels_list")


class HotelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Hotel
    template_name = "providers/hotel_update_form.html"
    fields = [
        "name",
        "stars",
        "description",
        "main_picture",
        "second_picture",
        "third_picture",
        "site_url",
        "google_maps_location",
        "contact_phone",
        "text_location",
    ]
    success_message = _("Hotel successfully updated.")

    def get_success_url(self):
        return reverse_lazy("providers:hotel_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Modificar {self.object.name}"
        return context


class HotelCreationWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ("0", HotelBasicInfoForm),
        ("1", HotelLocationForm),
        ("2", HotelImagesForm),
    ]

    template_name = "providers/wizards/hotel_wizard_form.html"
    file_storage = FileSystemStorage()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context["step_titles"] = {
            "0": _("Basic info"),
            "1": _("Location"),
            "2": _("Images"),
        }
        return context

    def get_step_url(self, step):
        """Genera la URL correcta del paso"""
        return reverse("hotel_create_wizard", kwargs={"step": step})

    def done(self, form_list, form_dict, **kwargs):
        hotel_data = {}
        for form in form_list:
            hotel_data.update(form.cleaned_data)

        valid_fields = [f.name for f in Hotel._meta.fields]
        filtered_data = {k: v for k, v in hotel_data.items() if k in valid_fields}

        if self.request.user.enterprise_account:
            filtered_data.update({"account": self.request.user.enterprise_account})

        hotel = Hotel.objects.create(**filtered_data, created_by=self.request.user)
        messages.info(self.request, _("Hotel created succsefully."))

        redirect_url = reverse("providers:hotel_detail", kwargs={"pk": hotel.pk})

        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = redirect_url
            return response

        return redirect(redirect_url)

    def render_next_step(self, form, **kwargs):
        """Renderiza solo el contenido del formulario si es una solicitud HTMX"""
        if self.request.headers.get("HX-Request"):
            # Cambiar el template para peticiones HTMX
            self.template_name = "providers/wizards/partials/hotel_wizard_form.html"
        response = super().render_next_step(form, **kwargs)
        return response

    def render(self, form=None, **kwargs):
        """Maneja el template correcto para peticiones HTMX"""
        if self.request.headers.get("HX-Request"):
            self.template_name = "providers/wizards/partials/hotel_wizard_form.html"
        return super().render(form, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Asigna un paso por defecto si no se recibe en la URL"""
        if "step" not in kwargs:
            return redirect(
                reverse("providers:hotel_create_wizard", kwargs={"step": "1"})
            )
        return super().dispatch(request, *args, **kwargs)


class RoomTypeCreationWizardView(SessionWizardView):
    form_list = [
        ("0", RoomTypeBasicInfoForm),
        ("1", RoomTypeCapacityForm),
        ("2", RoomTypeImagesForm),
    ]
    template_name = "providers/wizards/room_type_wizard_form.html"
    file_storage = FileSystemStorage()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context["step_titles"] = {
            "0": _("Basic info"),
            "1": _("Capacity"),
            "2": _("Images"),
        }
        context["hotel_id"] = self.kwargs["hotel_id"]
        return context

    def get_step_url(self, step):
        """Genera la URL correcta del paso"""
        return reverse("room_type_create_wizard", kwargs={"step": step})

    def done(self, form_list, **kwargs):
        # Procesar los datos del formulario
        room_type_data = {}
        for form in form_list:
            room_type_data.update(form.cleaned_data)

        # Crear RoomType
        room_type = RoomType.objects.create(
            **room_type_data,
            hotel_id=self.kwargs["hotel_id"],
            created_by=self.request.user,
        )

        response = HttpResponse()
        response["HX-Redirect"] = reverse(
            "providers:my_hotel_rooms_list",
            kwargs={"hotel_id": self.kwargs["hotel_id"]},
        )
        return response

    def render_next_step(self, form, **kwargs):
        """Conditional rending to manage HTMX requests"""
        if self.request.headers.get("HX-Request"):
            # Cambiar el template para peticiones HTMX
            self.template_name = "providers/wizards/partials/room_type_wizard_form.html"
        response = super().render_next_step(form, **kwargs)
        return response

    def render(self, form=None, **kwargs):
        """Template management for  HTMX requests"""
        if self.request.headers.get("HX-Request"):
            self.template_name = "providers/wizards/partials/room_type_wizard_form.html"
        return super().render(form, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Asigna un paso por defecto si no se recibe en la URL"""
        if "step" not in kwargs:
            return redirect(
                reverse("providers:room_type_create_wizard", kwargs={"step": "1"})
            )
        return super().dispatch(request, *args, **kwargs)


class MyHotelRoomsListView(LoginRequiredMixin, ListView):
    model = RoomType
    template_name = "providers/roomtypes_list.html"
    context_object_name = "hotels"
    paginate_by = 4

    def get_queryset(self):
        return self.model.objects.filter(
            created_by=self.request.user, hotel=self.kwargs["hotel_id"]
        ).order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hotel_id"] = self.kwargs["hotel_id"]
        context["title"] = _("Roomtypes.")
        return context


@method_decorator(csrf_exempt, name="dispatch")
class RoomTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = RoomType

    def get_success_url(self):
        return reverse_lazy(
            "providers:my_hotel_rooms_list", kwargs={"hotel_id": self.object.hotel.id}
        )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = success_url
            return response

        return HttpResponseRedirect(success_url)


class RoomTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = RoomType
    template_name = "providers/roomtype_update.html"
    fields = [
        "name",
        "description",
        "adults_capacity",
        "children_capacity",
        "stock",
        "is_available",
        "main_picture",
        "secondary_picture",
        "third_picture",
        "internal_notes",
    ]

    def get_success_url(self):
        return reverse_lazy("providers:roomtype_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Tipo de Habitación"
        return context


class RoomTypeDetailView(LoginRequiredMixin, DetailView):
    model = RoomType
    template_name = "providers/roomtype_detail.html"
    context_object_name = "room_type"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

    # Protects form outter users to view details.
    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)
