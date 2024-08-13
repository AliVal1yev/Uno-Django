from django import forms
from .models import Card

class PlayCardForm(forms.Form):
    card = forms.ModelChoiceField(queryset=Card.objects.all(), required=False)
    draw_card = forms.BooleanField(required=False)


class ColorChoiceForm(forms.Form):
    COLOR_CHOICES = [
        ('blue', 'Blue'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('green', 'Green'),
    ]
    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.RadioSelect)
