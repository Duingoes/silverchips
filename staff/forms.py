"""Custom forms for convenience.

Contains convenient intermediary forms for login and similar
applications.
"""

from django import forms
from django.utils import timezone
from core import models
from staff.widgets import RichTextWidget
from dal import autocomplete


# Form classes
class LoginForm(forms.Form):
    """A basic login form for staff and administrators."""

    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password")


class ContentForm(forms.ModelForm):
    """A generic editor for any kind of content."""

    class Meta:
        model = models.Content
        fields = ['title', 'authors', 'description']
        widgets = {
            'title': forms.widgets.TextInput(),
            'lead': RichTextWidget(short=True),
            'authors': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users")
        }
        abstract = True

    def save(self, commit=True):
        model = super(ContentForm, self).save(commit=False)
        model.modified = timezone.now()

        if commit:
            model.save()

        return model


class StoryForm(ContentForm):
    """The story editor form."""

    class Meta(ContentForm.Meta):
        model = models.Story
        fields = ContentForm.Meta.fields + ['lead', 'text']
        widgets = dict(ContentForm.Meta.widgets, text=RichTextWidget())


class ImageForm(ContentForm):
    """Form for image creation."""

    class Meta:
        model = models.Image
        fields = ['source']
