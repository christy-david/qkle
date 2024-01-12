from django import forms
from listing.models import Vehicle,Category
from listing.forms import MultipleFileInput
from ads.models import Ad

INPUT_CLASSES = 'block p-3 ps-5 appearance-none outline-none text-gray-900 text-sm font-medium w-full rounded placeholder-gray-900 border border-gray-900 mb-6'

class VehicleEditForm(forms.ModelForm):
    new_images = forms.ImageField(widget=MultipleFileInput(), required=False)  # Use the MultipleFileInput widget

    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'make': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
             'model': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'kms_driven': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'fuel_type': forms.RadioSelect(attrs={
                'class': ''
            }),
            'transmission': forms.RadioSelect(attrs={
                'class': ''
            }),
            'no_of_owners': forms.RadioSelect(attrs={
                'class': ''
            }),
            'location': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter your location'
            }),
            'registered_year': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'additional_details': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
        }

        def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Category Name'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'block p-3 ps-5 appearance-none outline-none text-gray-900 text-sm font-medium w-full rounded placeholder-gray-900 border border-gray-900 mb-6'}),
        }


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['image']