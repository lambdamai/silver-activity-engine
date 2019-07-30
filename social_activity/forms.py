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

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
            'class': 'form-control'
        })


class SocialGroup(forms.Form):
    inn = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(SocialGroup, self).__init__(*args, **kwargs)
        self.fields['inn'].widget.attrs.update({
            'class': 'form-control'
        })
