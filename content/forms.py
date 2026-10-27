from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave this field empty")

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "maxlength": 100}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "maxlength": 254}),
            "subject": forms.TextInput(attrs={"maxlength": 160}),
            "message": forms.Textarea(attrs={"rows": 6, "maxlength": 5000}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Your message could not be submitted.")
        return value

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please provide a little more detail (at least 10 characters).")
        return message
