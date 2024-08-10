from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking , Review ,Package

    
class BookingForm(forms.ModelForm):
    total_persons = forms.IntegerField(min_value=1, required=True)
    class Meta:
        model = Booking
        fields = ['start_date', 'total_persons']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Add any custom password validation here
        return password

# LoginForm for User Authentication
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['package', 'rating', 'comment']

    package = forms.ModelChoiceField(queryset=Package.objects.all(), required=True, label='Package')
    rating = forms.IntegerField(min_value=1, max_value=5, required=True, label='Rating (1-5)')
    comment = forms.CharField(widget=forms.Textarea, required=True, label='Comment')