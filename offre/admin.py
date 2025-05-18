from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Person)
admin.site.register(Media)
admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(Location)
admin.site.register(WorkOffer)
admin.site.register(OfferApplication)
admin.site.register(Recommender)
