from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import CustomUser
from .models import UserAddress

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number']

# class PasswordChangeForm(DjangoPasswordChangeForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your current password'})
#         self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a new password'})
#         self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm the new password'})

#     def clean_new_password2(self):
#         new_password1 = self.cleaned_data.get('new_password1')
#         new_password2 = self.cleaned_data.get('new_password2')
#         if new_password1 and new_password2 and new_password1 != new_password2:
#             raise forms.ValidationError("The two password fields didn't match.")
#         return new_password2

# class UserAddressForm(forms.ModelForm):
#     class Meta:
#         model = UserAddress
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'street', 'city', 'state', 'country', 'pincode', 'land_mark']


# class ChooseDefaultAddressForm(forms.Form):
#     address_id = forms.IntegerField(widget=forms.HiddenInput())


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')