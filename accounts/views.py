from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .form import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from dateutil.relativedelta import relativedelta
import datetime
from .filters import *
from .form import *
from django import forms


@login_required(login_url='login_page')
@admin_only
def dashboard(request):
	ongoing_donations=DonationHistory.objects.all().filter(status='In Process')
	hospitals=Hospital.objects.all()
	requests=Request.objects.all().filter(status='Pending')
	tdonor=Donor.objects.all().count()
	thospital=Hospital.objects.all().count()
	tprequest=Request.objects.all().filter(status='Pending').count()
	context={'od':ongoing_donations,'hospitals':hospitals,'requests':requests,
	'tdonor':tdonor,'thospital':thospital,'tprequest':tprequest}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login_page')
@donor_only
def my_dashboard_donor(request):
	donations=request.user.donor.donationhistory_set.all()
	cdonation=donations.count()
	adonation=donations.filter(status='Approved').count()
	rdonation=donations.filter(status='Rejected').count()
	name=request.user.donor.dname
	context={'donations':donations,'name':name,
	'cdonation':cdonation,'adonation':adonation,'rdonation':rdonation}
	return render(request,'accounts/my_dashboard_donor.html',context)

@login_required(login_url='login_page')
@hospital_only
def my_dashboard_hospital(request):
	requests=request.user.hospital.request_set.all()
	crequest=requests.count()
	frequest=requests.filter(status='Fulfilled').count()
	prequest=requests.filter(status='Pending').count()
	name=request.user.hospital.hname
	context={'requests':requests,'name':name,
	'crequest':crequest,'frequest':frequest,'prequest':prequest}
	return render(request,'accounts/my_dashboard_hospital.html',context)		


@redirect_if_hospital
def my_donor_profile(request):
	donor=request.user.donor
	donor.dage=(relativedelta(datetime.date.today(),donor.dob)).years
	context={'donor':donor}
	return render(request,'accounts/my_donor_profile.html',context)


@hospital_only
def my_hospital_profile(request):
	hospital=request.user.hospital
	context={'hospital':hospital}
	return render(request,'accounts/my_hospital_profile.html',context)



@login_required(login_url='login_page')
@admin_only
def donor_list(request):
	donors=Donor.objects.all()
	for i in donors:
		i.dage=(relativedelta(datetime.date.today(),i.dob)).years
	myfilter=DonorFilter(request.GET,queryset=donors)
	donors=myfilter.qs	
	context={'donors':donors,'myfilter':myfilter}
	return render(request,'accounts/donor_list.html',context)

@login_required(login_url='login_page')
@admin_only
def hospital_list(request):
	hospitals=Hospital.objects.all()
	#Add Pending Requests
	for i in hospitals:
		c=Request.objects.all().filter(hospital=i).count()
		i.trequest=c
	myfilter=HospitalFilter(request.GET,queryset=hospitals)
	hospitals=myfilter.qs		
	context={'hospitals':hospitals,'myfilter':myfilter}
	return render(request,'accounts/hospital_list.html',context)

@login_required(login_url='login_page')
@admin_only
def request_list(request):
	requests=Request.objects.all()
	myfilter=RequestFilter(request.GET,queryset=requests)
	requests=myfilter.qs
	context={'requests':requests,'myfilter':myfilter}
	return render(request,'accounts/request_list.html',context)


@login_required(login_url='login_page')
@admin_only
def blood_bag_list(request):
	bloodbags=BloodBag.objects.all()
	for i in bloodbags:
		i.crequest=Request.objects.all().filter(bloodgroup=i.bloodgroup,status='Pending').count()
	context={'bloodbags':bloodbags}
	return render(request,'accounts/blood_bag_list.html',context)


@login_required(login_url='login_page')
@admin_only
def donation_history(request):
	donationhistory=DonationHistory.objects.all()
	myfilter=DonationHistoryFilter(request.GET,queryset=donationhistory)
	donationhistory=myfilter.qs
	context={'donationhistory':donationhistory,'myfilter':myfilter}
	return render(request,'accounts/donation_history.html',context)		


@login_required(login_url='login_page')
@admin_only
def delete_donor(request,pk):
	donor=Donor.objects.get(did=pk)
	if request.method=="POST":
		user1=donor.user
		donor.delete()
		user1.delete()
		return redirect('admin_dashboard')
	context={'donor': donor}
	return render(request,'accounts/delete_donor.html',context)

@login_required(login_url='login_page')
def delete_hospital(request,pk):
	hospital=Hospital.objects.get(hid=pk)
	if request.method=="POST":
		user1=hospital.user
		hospital.delete()
		user1.delete()
		return redirect('admin_dashboard')
	context={'hospital': hospital}		
	return render(request,'accounts/delete_hospital.html',context)

@login_required(login_url='login_page')
@admin_only
def delete_request(request,pk):
	requests=Request.objects.get(rid=pk)
	if request.method=="POST":
		requests.delete()
		return redirect('admin_dashboard')
	context={'requests': requests}	
	return render(request,'accounts/delete_request.html',context)


@login_required(login_url='login_page')
@admin_only
def delete_bloodbag(request,pk):
	bloodbag=BloodBag.objects.get(bbid=pk)
	if request.method=="POST":
		bloodbag.delete()
		return redirect('admin_dashboard')
	context={'bloodbag': bloodbag}	
	return render(request,'accounts/delete_bloodbag.html',context)


@login_required(login_url='login_page')
@admin_only
def deliver_blood(request,pk):
	bloodbag=BloodBag.objects.get(bbid=pk)
	c=[]
	requests=Request.objects.all()
	for i in requests:
		if i.status!="Fulfilled" and i.bloodgroup==bloodbag.bloodgroup:
			c1=(i.rid,"Hospital:{} Request_ID:{} Priority:{} Received on: {}".format(i.hospital.hname,i.rid,i.comments,i.reqdate))
			c.append(c1)
	c=tuple(c)
	option=forms.ChoiceField(widget=forms.RadioSelect,choices=c)
	form=ChooseRequest()
	form.fields['option'].choices=c
	if request.method=="POST":
		form=ChooseRequest(request.POST)
		if form.is_valid():
			f=form.cleaned_data
			print(f['option'])
			req=Request.objects.get(rid=f['option'])
			req.status="Fulfilled"
			req.save()			
			print(req.status)
			bloodbag.delete()
			return redirect('admin_dashboard')
	context={'form':form,'bb':bloodbag}
	return render(request,'accounts/deliver_blood.html',context)


@login_required(login_url='login_page')
@admin_only
def donor_profile(request,pk):
	donor=Donor.objects.get(did=pk)
	donor.dage=(relativedelta(datetime.date.today(),donor.dob)).years
	donations=DonationHistory.objects.all().filter(donor=donor)
	c=donations.count()
	myfilter=DonationHistoryFilter(request.GET,queryset=donations)
	donations=myfilter.qs
	context={'donor':donor,'donations':donations,'c':c,'myfilter':myfilter}
	return render(request,'accounts/donor_profile.html',context)

@login_required(login_url='login_page')
@admin_only
def hospital_profile(request,pk):
	hospital=Hospital.objects.get(hid=pk)
	requests=Request.objects.all().filter(hospital=hospital)
	count_request=requests.count()
	myfilter=RequestFilter(request.GET,queryset=requests)
	requests=myfilter.qs
	context={'hospital':hospital,'requests':requests,'count_request':count_request,'myfilter':myfilter}
	return render(request,'accounts/hospital_profile.html',context)



@login_required(login_url='login_page')
@allowed_user(allowed_roles=['donor','admin'])
def update_donor_profile(request,pk):
	donor1=Donor.objects.get(did=pk)
	print(donor1)
	form1=UpdateDonor(instance=donor1)
	if request.method=="POST":
		form1=UpdateDonor(request.POST,instance=donor1)
		print("Hello")
		if form1.is_valid():
			form1.save()
			return redirect('admin_dashboard')
	context={'form1':form1,'donor':donor1}
	return render(request,'accounts/update_donor_profile.html',context)


@login_required(login_url='login_page')
@allowed_user(allowed_roles=['hospital','admin'])
def update_hospital_profile(request,pk):
	hospital=Hospital.objects.get(hid=pk)
	print(hospital)
	form1=UpdateHospital(instance=hospital)
	if request.method=="POST":
		form1=UpdateHospital(request.POST,instance=hospital)
		print("Hello")
		if form1.is_valid():
			form1.save()
			return redirect('admin_dashboard')
	context={'form1':form1,'hospital':hospital}
	return render(request,'accounts/update_hospital_profile.html',context)


@login_required(login_url='login_page')
@admin_only
def update_request(request,pk):
	requests=Request.objects.get(rid=pk)
	form=UpdateRequest(instance=requests)
	if request.method=='POST':
		form=UpdateRequest(request.POST,instance=requests)
		if form.is_valid():
			form.save()
			return redirect('admin_dashboard')
	context={'form':form,'request':requests}
	return render(request,'accounts/update_request.html',context)	


@login_required(login_url='login_page')
@admin_only
def update_donation(request,pk):
	donation=DonationHistory.objects.get(bid=pk)
	form=UpdateDonation(instance=donation)
	if request.method=='POST':
		form=UpdateDonation(request.POST,instance=donation)
		if form.is_valid():
			f=form.cleaned_data
			if f['status']=="Approved":
				BloodBag.objects.create(bbid="BB"+donation.bid[2:],bloodgroup=donation.bloodgroup,
					quantity=donation.quantity,donatedate=donation.donatedate,expirydate=donation.expirydate,donor=donation.donor)
			print(form.cleaned_data)
			print(donation)
			form.save()
			return redirect('admin_dashboard')
	context={'form':form,'donation':donation}
	return render(request,'accounts/update_donation.html',context)			


@unauthenticated_user
def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username1')
		password =request.POST.get('password1')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('admin_dashboard')
		else:
			messages.info(request, 'Username OR password is incorrect')
			return redirect('login_page')
	context={}
	return render(request,'accounts/login_page.html',context)



def logoutUser(request):
	logout(request)
	return redirect('login_page')



@login_required(login_url='login_page')
@admin_only
def register_page_donor(request):
	form1=DonorForm()
	form2=CreateUserForm()
	if request.method=="POST":
		form1=DonorForm(request.POST)
		form2=CreateUserForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			f1=form1.cleaned_data
			#user=form2.cleaned_data.get('username')
			user=form2.save()
			group=Group.objects.get(name='donor')
			user.groups.add(group)
			Donor.objects.create(user=user,did=f1['did'],dname=f1['dname'],dgender=f1['dgender'],
				dage=f1['dage'],daddress=f1['daddress'],dphone=f1['dphone'],demail=f1['demail'],
				dweight=f1['dweight'],dob=f1['dob'])
			return redirect('login_page')
	context={'form1':form1,'form2':form2}
	return render(request,'accounts/register_page_donor.html',context)


@login_required(login_url='login_page')
@admin_only
def register_page_hospital(request):
	form1=HospitalForm()
	form2=CreateUserForm()
	if request.method=="POST":
		form1=HospitalForm(request.POST)
		form2=CreateUserForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			f1=form1.cleaned_data
			#user=form2.cleaned_data.get('username')
			form2.save()
			user=form2.save()
			group=Group.objects.get(name='hospital')
			user.groups.add(group)
			Hospital.objects.create(user=user,hid=f1['hid'],hname=f1['hname'],
				haddress=f1['haddress'],hphone=f1['hphone'],hemail=f1['hemail'])
			return redirect('login_page')
	context={'form1':form1,'form2':form2}
	return render(request,'accounts/register_page_hospital.html',context)


@login_required(login_url='login_page')
@admin_only
def create_blood_sample(request,pk):
	d=Donor.objects.get(did=pk)
	form=CreateDonation()
	if request.method=="POST":
		form=CreateDonation(request.POST)
		if form.is_valid():
			form.save()
			return redirect('admin_dashboard')
	context={'form':form,'d':d}
	return render(request,'accounts/create_blood_sample.html',context)


@login_required(login_url='login_page')
@allowed_user(allowed_roles=['hospital','admin'])
def create_requests(request,pk):
	h=Hospital.objects.get(hid=pk)
	form=CreateRequest()
	if request.method=="POST":
		form=CreateRequest(request.POST)
		if form.is_valid():
			form.save()
			return redirect('admin_dashboard')
	context={'form':form,'h':h}
	return render(request,'accounts/create_requests.html',context)



														