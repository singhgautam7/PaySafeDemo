import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Mandatory. This will be used as username')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email


class PaymentForm(forms.Form):
    mobile = forms.IntegerField(required=False)

    street = forms.CharField(max_length=2000, required=False)
    city = forms.CharField(max_length=50, required=False)
    pincode = forms.IntegerField(required=False)

    amount = forms.DecimalField(decimal_places=2, required=True)

    is_submit_clicked = forms.IntegerField(initial=0, widget=forms.HiddenInput())
    paysafe_user_id = forms.CharField(max_length=50, widget=forms.HiddenInput(), required=False)

    # A hidden input for internal use tell from which page the user sent the message

    # def clean(self):
    #     cleaned_data = super(PaymentForm, self).clean()
    #     first_name = cleaned_data.get('first_name')
    #     mobile = cleaned_data.get('mobile')
    #     amount = cleaned_data.get('amount')
    #     if not first_name and not amount and not mobile:
    #         raise forms.ValidationError('You have to write something!')

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if mobile is not None:
            if len(str(mobile)) != 10:
                raise forms.ValidationError("Number should be 10 digits only")

        return mobile

    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        if pincode is not None:
            if len(str(pincode)) != 6:
                raise forms.ValidationError("Pincode should be 6 digits only")

        elif pincode is None or pincode == '':
            raise forms.ValidationError("Required for billing address")
        return pincode

    def clean_city(self):
        city = self.cleaned_data['city']
        if city is None or city == '':
            raise forms.ValidationError("Required for billing address")
        return city

    def clean_address(self):
        address = self.cleaned_data['address']
        if address is None or address == '':
            raise forms.ValidationError("Required for billing address")

        # if not re.findall('[^A-Za-z0-9]', address):
        #     raise forms.ValidationError("Special characters are not allowed")
        return address
