from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from formtools.wizard.views import SessionWizardView

from staytrade.providers.forms import (
    RoomTypeBasicInfoForm,
    RoomTypeCapacityForm,
    RoomTypeImagesForm,
)
from staytrade.providers.models import RoomType
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _


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


class RoomTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
    success_message = _("Room type successfully updated.")

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
