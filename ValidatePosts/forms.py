from django import forms
from .models import Post
from django_ckeditor_5.widgets import CKEditor5Widget

class StudentReviewForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }

class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "status", "feedback"]
        widgets = {
            "body": CKEditor5Widget(config_name="default"),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "feedback": forms.Textarea(attrs={"class": "form-control"}),
        }
class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Título del post",
            "class": "form-control"
        })
    )

    imgs = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    tags = forms.CharField(
        required=False,
        label="Etiquetas",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: deportes, ciencia, concursos"
        })
    )
    class Meta:
        model = Post
        fields = ["title", "body", "imgs", "tags", "links", "attachment", "video_url"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return title
