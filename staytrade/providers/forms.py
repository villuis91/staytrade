# hotels/forms.py
from django import forms
from .models import Hotel, RoomType, RoomTypeAvailability


# Hotel wizard forms
class HotelBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "description", "stars"]


class HotelLocationForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["text_location", "contact_phone", "google_maps_location", "site_url"]


class HotelImagesForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["main_picture", "second_picture", "third_picture"]


# Room type wizard form
class RoomTypeBasicInfoForm(forms.ModelForm):
    """Paso 1: Información básica"""

    class Meta:
        model = RoomType
        fields = ["name", "description", "is_available", "internal_notes"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "internal_notes": forms.Textarea(attrs={"rows": 3}),
        }


class RoomTypeCapacityForm(forms.ModelForm):
    """Paso 2: Capacidad y número de habitaciones"""

    class Meta:
        model = RoomType
        fields = ["adults_capacity", "children_capacity", "stock"]
        widgets = {
            "adults_capacity": forms.NumberInput(attrs={"min": 1}),
            "children_capacity": forms.NumberInput(attrs={"min": 0}),
            "stock": forms.NumberInput(attrs={"min": 1}),
        }


class RoomTypeImagesForm(forms.ModelForm):
    """Paso 3: Imágenes"""

    class Meta:
        model = RoomType
        fields = ["main_picture", "secondary_picture", "third_picture"]
        widgets = {
            "main_picture": forms.FileInput(attrs={"class": "form-control"}),
            "secondary_picture": forms.FileInput(attrs={"class": "form-control"}),
            "third_picture": forms.FileInput(attrs={"class": "form-control"}),
        }


class RoomTypeAvailabilityForm(forms.ModelForm):
    """Paso 4: Disponibilidad inicial"""

    class Meta:
        model = RoomTypeAvailability
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
