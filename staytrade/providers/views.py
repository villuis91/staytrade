from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.urls import reverse
from staytrade.providers.models import Hotel
from staytrade.providers.forms import (
    HotelBasicInfoForm,
    HotelLocationForm,
    HotelImagesForm,
)
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class HotelDetailView(LoginRequiredMixin, DetailView):
    model = Hotel
    template_name = "providers/hotel_detail.html"
    context_object_name = "hotel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
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

    def done(self, form_list, form_dict, **kwargs):
        hotel_data = {}
        for form in form_list:
            hotel_data.update(form.cleaned_data)

        # Filtrar campos que no están en el modelo
        valid_fields = [f.name for f in Hotel._meta.fields]
        filtered_data = {k: v for k, v in hotel_data.items() if k in valid_fields}

        hotel = Hotel.objects.create(**filtered_data, created_by=self.request.user)

        messages.info(self.request, "Hotel creado correctamente.")
        return redirect(reverse("providers:hotel_detail", kwargs={"pk": hotel.pk}))
