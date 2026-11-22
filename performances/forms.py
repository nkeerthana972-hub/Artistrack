from django import forms
from .models import Performance


class PerformanceForm(forms.ModelForm):

    class Meta:
        model = Performance

        fields = '__all__'

        widgets = {

            'performance_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

        }