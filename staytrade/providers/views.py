from django.contrib.auth.mixins import LoginRequiredMixin
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
)
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin


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


class HotelDeleteView(DeleteView):
    model = Hotel
    success_url = reverse_lazy("providers:my_hotels_list")


class HotelUpdateView(SuccessMessageMixin, UpdateView):
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
        print(self.request.user.enterprise_account)
        if self.request.user.enterprise_account:
            filtered_data.update({"account": self.request.user.enterprise_account})
            print(filtered_data)

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
            self.template_name = "providers/wizards/partials/wizard_form.html"
        response = super().render_next_step(form, **kwargs)
        return response

    def render(self, form=None, **kwargs):
        """Maneja el template correcto para peticiones HTMX"""
        if self.request.headers.get("HX-Request"):
            self.template_name = "providers/wizards/partials/wizard_form.html"
        return super().render(form, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Asigna un paso por defecto si no se recibe en la URL"""
        if "step" not in kwargs:
            return redirect(
                reverse("providers:hotel_create_wizard", kwargs={"step": "1"})
            )
        return super().dispatch(request, *args, **kwargs)


class HotelTypeDetailView(LoginRequiredMixin, DetailView):
    pass
