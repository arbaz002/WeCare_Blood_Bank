from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Donor)
admin.site.register(Hospital)
admin.site.register(BloodBag)
admin.site.register(Request)
admin.site.register(DonationHistory)