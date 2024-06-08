from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Blog, Tag

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        exclude = ['slug', 'date', 'active', 'top', 'is_main', 'views_num', 'user','tags','is_remove']



