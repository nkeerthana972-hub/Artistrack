from django import forms

from .models import Training


class TrainingForm(forms.ModelForm):

    class Meta:

        model = Training

        fields = '__all__'

        widgets = {

            'session_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter session title'
            }),

            'trainer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter trainer name'
            }),

            'training_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter training type'
            }),

            'training_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in hours'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter notes or coach feedback'
            }),

        }