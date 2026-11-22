from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from captcha.fields import CaptchaField
from django.contrib.auth.forms import PasswordChangeForm

class RegisterForm(UserCreationForm):

    captcha = CaptchaField()

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="""
        Password must contain:
        - At least 12 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number
        - At least 1 special character (@$!%*?&)
        """
    )



    class Meta:

        model = CustomUser

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
    
    def save(self, commit=True):

        user = super().save(commit=False)

        # PUBLIC REGISTER = ARTIST ONLY
        user.role = 'artist'

        if commit:
            user.save()

        return user

from django.contrib.auth.forms import AuthenticationForm

# =========================
# LOGIN FORM
# =========================

class LoginForm(AuthenticationForm):

    captcha = CaptchaField()

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

# =========================
# ADMIN CREATES STAFF
# =========================

class StaffCreateForm(UserCreationForm):

    class Meta:

        model = CustomUser

        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # REMOVE ADMIN OPTION
        self.fields['role'].choices = [
            ('director', 'Director'),
            ('coach', 'Coach'),
        ]

        # STYLING

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['role'].widget.attrs.update({
            'class': 'form-select'
        })

# =========================
# OTP FORM
# =========================

class OTPForm(forms.Form):

    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6 digit OTP'
        })
    )

class CustomPasswordChangeForm(
    PasswordChangeForm
):
    captcha = CaptchaField()

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

class ForgotPasswordForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })
    )
    captcha = CaptchaField()



 