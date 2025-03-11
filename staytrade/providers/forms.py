# hotels/forms.py
from django.forms import ModelForm, IntegerField, NumberInput
from .models import Hotel


class HotelBasicInfoForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "description", "stars"]


class HotelLocationForm(ModelForm):
    stars = IntegerField(
        min_value=1,
        max_value=5,
        widget=NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Hotel
        fields = ["text_location", "contact_phone", "google_maps_location", "site_url"]


class HotelImagesForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ["main_picture", "second_picture", "third_picture"]
