# hotels/forms.py
from django.forms import ModelForm
from .models import Hotel


class HotelBasicInfoForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "description", "stars"]


class HotelLocationForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ["google_maps_location", "site_url"]


class HotelImagesForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ["main_picture", "second_picture", "third_picture"]
