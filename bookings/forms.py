from django import forms
from .models import Booking, PickupPoint, DestinationPoint

class BookingForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=PickupPoint.objects.all())
    destination = forms.ModelChoiceField(queryset=DestinationPoint.objects.none())

    def __init__(self, *args, **kwargs):
        origin_id = kwargs.pop('origin_id', None)
        super().__init__(*args, **kwargs)
        if origin_id:
            self.fields['destination'].queryset = DestinationPoint.objects.filter(origin_id=origin_id)

from django import forms
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['name', 'mobile', 'gender', 'age', 'username']
