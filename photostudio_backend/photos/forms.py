from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com'}),
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Your phone number'}),
    )
    service = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Select(),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Tell me about your project and requirements...',
        }),
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'Preferred Date',
        }),
        label='Preferred Date (Optional)',
    )
    source = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, service_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('', 'Select a service')]
        if service_choices:
            choices.extend(service_choices)
        self.fields['service'].widget = forms.Select(
            choices=choices,
            attrs={'class': 'form-select'},
        )
