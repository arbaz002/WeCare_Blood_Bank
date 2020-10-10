import django_filters
from django_filters import DateFilter
from .models import *

class DonationHistoryFilter(django_filters.FilterSet):
	start_date=DateFilter(field_name='donatedate',lookup_expr='gte')
	class Meta:
		model=DonationHistory
		fields=['status']

class RequestFilter(django_filters.FilterSet):
	class Meta:
		model=Request
		fields=['status']		


class DonorFilter(django_filters.FilterSet):
	class Meta:
		model=Donor
		fields=['did','dname','dgender','dage']	


class HospitalFilter(django_filters.FilterSet):
	class Meta:
		model=Hospital
		fields=['hid','hname']	