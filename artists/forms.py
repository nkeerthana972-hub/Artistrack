from django import forms
from .models import Artist


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist

        fields = '__all__'


        

class ArtistProfileForm(forms.ModelForm):

    class Meta:

        model = Artist

        fields = [
            'first_name',
            'last_name',
            'age',
            'gender',
            'dance_style',
            'phone',
            'email',
            'profile_image'
        ]

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            'dance_style': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

        }
