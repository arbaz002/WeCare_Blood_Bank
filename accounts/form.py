from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.forms import widgets


def get_list():
	r=Request.objects.all()
	c=[]
	for i in r:
		c.append((i.rid,i.rid))
	c=tuple(c)
	print(c)
	return c




class DonorForm(forms.Form):
	Gender=(('Male','Male'),('Female','Female'),('Others','Others'))
	did=forms.CharField(label='did',widget=forms.TextInput(attrs={'placeholder':'D000__'}))
	dname=forms.CharField(label='dname',widget=forms.TextInput(attrs={'placeholder':'Name'}))
	dgender=forms.ChoiceField(widget=forms.RadioSelect,choices=Gender)
	dage=forms.IntegerField(label='dage',widget=forms.NumberInput(attrs={'placeholder':'Age'}))
	daddress=forms.CharField(label='daddress',widget=forms.Textarea(attrs={'placeholder':'Address'}))
	dphone=forms.CharField(label='dphone',widget=forms.TextInput(attrs={'placeholder':'Phone No.'}))
	demail=forms.EmailField(label='demail',widget=forms.EmailInput(attrs={'placeholder':'Email'}))
	dweight=forms.IntegerField(label='dweight',widget=forms.NumberInput(attrs={'placeholder':'Weight(in kg)'}))
	dob=forms.DateField(label='dob',widget=forms.DateInput(attrs={'placeholder':'DOB: YYYY-MM-DD'}))

class HospitalForm(forms.Form):
	hid=forms.CharField(label='did',widget=forms.TextInput(attrs={'placeholder':'H000__'}))
	hname=forms.CharField(label='dname',widget=forms.TextInput(attrs={'placeholder':'Name'}))
	haddress=forms.CharField(label='daddress',widget=forms.Textarea(attrs={'placeholder':'Address'}))
	hphone=forms.CharField(label='dphone',widget=forms.TextInput(attrs={'placeholder':'Phone No.'}))
	hemail=forms.EmailField(label='demail',widget=forms.EmailInput(attrs={'placeholder':'Email'}))	

class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','password1','password2']	


class UpdateDonor(ModelForm):
	class Meta:
		model=Donor
		fields='__all__'
		exclude=['user','did','dage']


class UpdateHospital(ModelForm):
	class Meta:
		model=Hospital
		fields='__all__'
		exclude=['user','hid','trequest']	


class UpdateRequest(ModelForm):
	class Meta:
		model=Request
		fields=['amount','comments','status']		


class CreateDonation(ModelForm):
	class Meta:
		model=DonationHistory
		fields='__all__'
		exclude=['status']


class UpdateDonation(ModelForm):
	class Meta:
		model=DonationHistory
		fields=['quantity','status']	


class CreateRequest(ModelForm):
	class Meta:
		model=Request
		fields='__all__'
		exclude=['status']

		

class ChooseRequest(forms.Form):	
	def __init__(self,*args,**kwargs):
		super(ChooseRequest, self ).__init__(*args, **kwargs)
		self.fields['option']=forms.ChoiceField(widget=forms.RadioSelect,choices=get_list())	