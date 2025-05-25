from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(Media)
