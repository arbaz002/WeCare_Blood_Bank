from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
	def wrapper_func(request,*args,**kwags):
		if request.user.is_authenticated:
			return redirect('admin_dashboard')
		else:
			return view_func(request,*args,**kwags)
	return wrapper_func



def allowed_user(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request,*args,**kwags):
			group=None
			if request.user.groups.exists():
				group=request.user.groups.all()[0].name	
			if group in allowed_roles:
				return view_func(request,*args,**kwags)
			elif group=='donor':
				return redirect("my_dashboard_donor")
			elif group=='hospital':
				return redirect('my_dashboard_hospital')	
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_func(request,*args,**kwags):
		group=""
		if request.user.groups.exists():
			group=request.user.groups.all()[0].name
		if group=="admin":
			return view_func(request,*args,**kwags)
		elif group=="donor":
			return redirect('my_dashboard_donor')
		elif group=="hospital":
			return redirect('my_dashboard_hospital')
	return wrapper_func



def hospital_only(view_func):
	def wrapper_func(request,*args,**kwags):
		group=""
		if request.user.groups.exists():
			group=request.user.groups.all()[0].name
		if group=="hospital":
			return view_func(request,*args,**kwags)
		elif group=="admin":
			return redirect('admin_dashboard')
		elif group=="donor":
			return redirect('my_dashboard_donor')	
	return wrapper_func



def donor_only(view_func):
	def wrapper_func(request,*args,**kwags):
		group=""
		if request.user.groups.exists():
			group=request.user.groups.all()[0].name
		if group=="donor":
			return view_func(request,*args,**kwags)
		elif group=="admin":
			return redirect('admin_dashboard')
		elif group=="hospital":
			return redirect('my_dashboard_hospital')	
	return wrapper_func	



def redirect_if_hospital(view_func):
	def wrapper_func(request,*args,**kwags):
		group=""
		if request.user.groups.exists():
			group=request.user.groups.all()[0].name
		if group=="donor":
			return view_func(request,*args,**kwags)
		elif group=="admin":
			return redirect('admin_dashboard')
		elif group=="hospital":
			return redirect('my_hospital_profile')	
	return wrapper_func					