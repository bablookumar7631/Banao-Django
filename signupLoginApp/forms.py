from django import forms
from .models import UserProfile


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    DESIGNATION_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'password', 'confirm_password', 'address_line1', 'city', 'state', 'pincode']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'address_line1': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match."
            )

        return cleaned_data




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())