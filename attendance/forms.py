from django import forms

from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:

        model = Attendance

        fields = '__all__'

        widgets = {

            'artist': forms.Select(attrs={
                'class': 'form-select'
            }),

            'training': forms.Select(attrs={
                'class': 'form-select'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional attendance remarks'
            }),

        }