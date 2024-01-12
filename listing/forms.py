from django import forms
# from django.forms.widgets import ClearableFileInput

from .models import Vehicle,Image

INPUT_CLASSES = 'block p-3 ps-5 appearance-none outline-none text-gray-900 text-sm font-medium w-full rounded placeholder-gray-900 border border-gray-900 mb-6'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.setdefault('class', f'{INPUT_CLASSES}')
        super().__init__(attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        kwargs.setdefault("label", "Images")
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImageForm(forms.Form):
    image = MultipleFileField()

    class Meta:
        model=Image
        fields=('image')

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('make','model','price','category','kms_driven','fuel_type','transmission','no_of_owners','location','registered_year','additional_details')
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

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        kms_driven = cleaned_data.get('kms_driven')

        if price is not None and kms_driven is not None:
            if price < 0 or kms_driven < 0:
                raise forms.ValidationError("Please enter non-negative values for price and kms_driven.")

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('make','model','price','category','kms_driven','fuel_type','transmission','no_of_owners','location','registered_year','additional_details', 'is_sold')
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
                'class': INPUT_CLASSES
            }),
            'registered_year': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'additional_details': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        kms_driven = cleaned_data.get('kms_driven')

        if price is not None and kms_driven is not None:
            if price < 0 or kms_driven < 0:
                raise forms.ValidationError("Please enter non-negative values for price and kms driven.")