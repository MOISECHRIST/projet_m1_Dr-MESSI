from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Person)
admin.site.register(ServicesProvided)
admin.site.register(PreferenceArea)
admin.site.register(Customer)
admin.site.register(Experience)
admin.site.register(Worker)
admin.site.register(MultipleQuestionAnswer)
admin.site.register(Evaluation)
admin.site.register(EvaluationAnswer)
