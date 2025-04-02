from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from staytrade.providers.models import MealPlan, RoomTypeMealPlan, RoomTypeMealPlanPrice
from .mixins import HotelContextMixin


class MealPlanListView(LoginRequiredMixin, HotelContextMixin, ListView):
    model = MealPlan
    template_name = "providers/meal_plans/list.html"
    context_object_name = "meal_plans"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(hotel=self.get_hotel_id()).order_by("name")


class MealPlanCreateView(
    LoginRequiredMixin, SuccessMessageMixin, HotelContextMixin, CreateView
):
    model = MealPlan
    template_name = "providers/meal_plans/form.html"
    fields = ["name", "details"]
    success_message = _("Meal plan successfully created.")

    def form_valid(self, form):
        form.instance.hotel_id = self.get_hotel_id()
        return super().form_valid(form)


class MealPlanUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, HotelContextMixin, UpdateView
):
    model = MealPlan
    template_name = "providers/meal_plans/form.html"
    fields = ["name", "details"]
    success_message = _("Plan de comidas actualizado exitosamente.")


class MealPlanDetailView(LoginRequiredMixin, HotelContextMixin, DetailView):
    model = MealPlan
    template_name = "providers/meal_plans/detail.html"
    context_object_name = "meal_plan"


class MealPlanDeleteView(LoginRequiredMixin, HotelContextMixin, DeleteView):
    model = MealPlan
    template_name = "providers/meal_plans/confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = self.get_success_url()
        return response
