from django.urls import reverse


class HotelContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hotel_id"] = self.get_hotel_id()
        return context

    def get_hotel_id(self):
        """
        Obtiene el hotel_id ya sea de kwargs (para vistas con hotel_id en URL)
        o del objeto (para vistas de detalle/actualización)
        """
        if hasattr(self, "object") and self.object:
            return self.object.hotel_id
        return self.kwargs.get("hotel_id")

    def get_success_url(self):
        """
        URL de redirección después de operaciones exitosas
        """
        hotel_id = self.get_hotel_id()
        return reverse("providers:meal_plan_list", kwargs={"hotel_id": hotel_id})
