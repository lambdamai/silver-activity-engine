from django import forms


class ActivityForm(forms.Form):
    choices = (
        ("eat-drink", "Еда и напитки"),
        ("restaurant", "Рестораны"),
        ("bookshop", "Книжный"),
    )
    lng = forms.CharField(widget=forms.HiddenInput())
    lat = forms.CharField(widget=forms.HiddenInput())
    category = forms.ChoiceField(choices=choices)
