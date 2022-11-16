from django import forms

# Reordering Form and View


class PositionForm(forms.ModelForm):
    position = forms.CharField()
