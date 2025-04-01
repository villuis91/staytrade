from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


# Main area
class MyAreaView(LoginRequiredMixin, TemplateView):
    template_name = "providers/providers_area.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            # Redirigir a una URL específica en lugar de renderizar el template
            response["HX-Redirect"] = self.request.build_absolute_uri(
                reverse("providers:my_area")
            )
            return response
        return super().render_to_response(context, **response_kwargs)


class HotelManagementView(LoginRequiredMixin, TemplateView):
    template_name = "providers/hotel_management_area.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            # Redirigir a una URL específica en lugar de renderizar el template
            response["HX-Redirect"] = self.request.build_absolute_uri(
                reverse("providers:hotel_management")
            )
            return response
        return super().render_to_response(context, **response_kwargs)
