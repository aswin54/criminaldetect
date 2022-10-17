from django import forms
from django.contrib.auth.forms import UserCreationForm

from detection_app.models import Login, Criminaldata, Missingdata


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('name', 'contact_no', 'email', 'username', 'password1', 'password2')


class LoginUpdate(UserCreationForm):
    class Meta:
        model = Login
        fields = ('name', 'contact_no', 'email', 'username', 'password1', 'password2')


class PoliceForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('first_name', 'last_name', 'username', 'contact_no', 'email','designation','district','station', 'password1', 'password2')


class PoliceUpdate(UserCreationForm):
    class Meta:
        model = Login
        fields = ('first_name', 'last_name', 'username', 'contact_no', 'email', 'password1', 'password2')


CRIME_TYPES = (
    ('Drug crimes', 'Drug crimes'),
    ('Street crime', 'Street crime'),
    ('Organized crime', 'Organized crime'),
    ('Political crime', 'Political crime'),
    ('Victimless crime', 'Victimless crime'),
    ('Other Crime', 'Other Crime'),
)


class CriminalForm(forms.ModelForm):
    crime = forms.CharField(widget=forms.Select(choices=CRIME_TYPES))

    class Meta:
        model = Criminaldata
        fields = '__all__'


gender_choice = (
    ("Male", "Male"),
    ("Female", "Female")
)


class MissingForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=gender_choice, required=True, widget=forms.RadioSelect)
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Missingdata
        fields = '__all__'
