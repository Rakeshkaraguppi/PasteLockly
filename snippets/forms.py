from django import forms

class SnippetForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Text Snippet')
    secret_key = forms.CharField(max_length=32, required=False, label='Secret Key (Optional)')
