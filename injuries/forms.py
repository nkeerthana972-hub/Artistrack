from django import forms
from .models import Injury


class InjuryForm(forms.ModelForm):

    class Meta:
        model = Injury

        fields = '__all__'

        widgets = {

            'injury_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

        }