from django.contrib.auth.mixins import LoginRequiredMixin

# from django.views.generic import RedirectView
# from django.urls import reverse
#
# class UserRedirectView(LoginRequiredMixin, RedirectView):
#     permanent = False
#
#     def get_redirect_url(self) -> str:
#         return reverse("users:detail", kwargs={"username": self.request.user.username})
#
#
# user_redirect_view = UserRedirectView.as_view()
