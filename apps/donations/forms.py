from django import forms

from apps.donations.models import Donation, Institution


class DonationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['institution'].empty_label = None

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.request.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Donation
        fields = ('quantity', 'categories', 'institution', 'address', 'phone_number',
                  'city', 'zip_code', 'pick_up_date', 'pick_up_time', 'pick_up_comment',)
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
            'institution': forms.RadioSelect,
        }
