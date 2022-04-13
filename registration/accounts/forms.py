from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User,Attendee,Organizer

class AttendeeSignUpForm(UserCreationForm):
    first_name= forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    dob=forms.DateField(required=True)
    class Meta(UserCreationForm.Meta):
        model=User

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_attendee=True
        user.first_name=self.cleaned_data('first_name')
        user.last_name=self.cleaned_data('last_name')
        user.save()
        attendee=Attendee.objects.create(user=user)
        
        attendee.email=self.cleaned_data.get('email')
        attendee.dob=self.cleaned_data.get('dob')
        attendee.save()
        return user


class OrganizerSignUpForm(UserCreationForm):
    first_name= forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    phone_number=forms.CharField(required=True)
    email=forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model=User
    
    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_organizer=True
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.save()
        organizer=Organizer.objects.create(user=user)
        
        organizer.phone_number=self.cleaned_data.get('phone_number')
        organizer.email=self.cleaned_data.get('email')
        organizer.save()
        return user