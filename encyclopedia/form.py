from .util import list_entries
from django import forms
import re

class NewPage(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in list_entries():
            raise forms.ValidationError('Entry with this title already exists, try again')
        return title

    def save_entry_to_file(self, title, entry):
        with open(f".entries/{title}.md", 'x') as f:
            f.write(f'# {title}\n' + entry)