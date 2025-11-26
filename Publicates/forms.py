from django import forms

class SupportForm(forms.Form):
    title = forms.CharField(max_length=255, label="Título")
    description = forms.CharField(widget=forms.Textarea, label="Descripción del problema")
