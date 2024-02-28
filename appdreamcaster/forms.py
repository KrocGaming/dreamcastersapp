from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))



class CustomerEnquireForm(forms.ModelForm):

    class Meta:
        model = CustomerEnqiuery
        fields = ['name','destination','date_of_travel','phone_number','group','package']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'destination': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'date_of_travel': forms.DateInput(
                attrs={
                    'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control' }
            ),
            'phone_number': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
                 'group': forms.Select(
                attrs={
                    'class': 'form-control'
                    }
                ),
                 'package': forms.Select(
                attrs={
                    'class': 'form-control'
                    }
                ),
         }
        

class CustomerDetailsForm(forms.ModelForm):

    class Meta:
        model = CustomerDetails
        fields = ['borading','destination','date']
        widgets = {
            'borading': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'destination': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
        }


class PassangerForm(forms.ModelForm):
    class Meta:
        CHOICES = (
            ('Male', 'Male'),
            ('Female', 'Female'),
        )
        model = Passenger
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'gender': forms.Select(choices=CHOICES,
                                   attrs={
                                       'class': 'form-control'
                                   }
                                   ),
        }


class PassangerDocForm(forms.ModelForm):
    class Meta:
        model = PassengerDoc
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'id_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
        }

        

PassengerDetailsFormSet = inlineformset_factory(
    CustomerDetails, Passenger, form=PassangerForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)
PassengerdocFormSet = inlineformset_factory(
    CustomerDetails, PassengerDoc, form=PassangerDocForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)