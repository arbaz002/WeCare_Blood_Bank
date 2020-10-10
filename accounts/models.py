from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Donor(models.Model):
	Gender=(('Male','Male'),('Female','Female'),('Others','Others'))
	user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	did=models.CharField(max_length=200,primary_key=True)
	dname=models.CharField(max_length=200,null=True)
	dgender=models.CharField(max_length=200,null=True,choices=Gender)
	dage=models.IntegerField(default=0)
	dob=models.DateField(default=datetime.date.today())
	dweight=models.IntegerField(null=True)
	daddress=models.CharField(max_length=200,null=True)
	dphone=models.CharField(max_length=200,null=True)
	demail=models.EmailField(max_length=200,null=True)

	def __str__(self):
		return self.dname


class Hospital(models.Model):
	user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	hid=models.CharField(max_length=200,primary_key=True)
	hname=models.CharField(max_length=200,null=True)
	haddress=models.CharField(max_length=200,null=True)
	hphone=models.CharField(max_length=200,null=True)
	hemail=models.EmailField(max_length=200,null=True)
	trequest=models.IntegerField(default=0)
	def __str__(self):
		return self.hname



class BloodBag(models.Model):
	bbid=models.CharField(max_length=200,primary_key=True)
	bloodgroup=models.CharField(max_length=10,null=True)
	quantity=models.IntegerField()
	donatedate=models.DateField()
	expirydate=models.DateField()
	crequest=models.IntegerField(default=0)
	donor=models.ForeignKey(Donor,on_delete=models.CASCADE)


class Request(models.Model):
	Priority=(('Standard','Standard'),('Urgent','Urgent'),('Critical','Critical'))
	Status=(('Fulfilled','Fulfilled'),('Pending','Pending'),('Rejected','Rejected'))
	rid=models.CharField(max_length=200,primary_key=True)
	bloodgroup=models.CharField(max_length=10,null=True)
	amount=models.IntegerField()
	comments=models.CharField(max_length=200,null=True,choices=Priority)
	status=models.CharField(max_length=200,null=True,choices=Status,default='Pending')
	hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
	reqdate=models.DateField(default=datetime.date.today())


class DonationHistory(models.Model):
	Status=(('Approved','Approved'),('Rejected','Rejected'),('In Process','In Process'))
	bid=models.CharField(max_length=200,primary_key=True)
	bloodgroup=models.CharField(max_length=10,null=True)
	quantity=models.IntegerField()
	donatedate=models.DateField(default=datetime.date.today())
	expirydate=models.DateField(default=datetime.date.today()+datetime.timedelta(days=42))
	donor=models.ForeignKey(Donor,on_delete=models.CASCADE)	
	status=models.CharField(max_length=200,null=True,choices=Status,default='In Process')

