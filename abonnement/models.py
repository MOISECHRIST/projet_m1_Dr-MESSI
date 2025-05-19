from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    LOGIN_STATUS = [("Logout", "Logout"),
                    ("Login", "Login")]

    USER_TYPE = [
        ("Customer", "Customer"),
        ("Worker", "Worker")
    ]
    id_person = models.IntegerField(unique=True, blank=False, null=False, primary_key=True)
    id_user = models.IntegerField(unique=True, blank=False, null=False)
    login_status = models.CharField(choices=LOGIN_STATUS, max_length=10, blank=False, null=False, default="Login")
    user_type = models.CharField(max_length=20, choices=USER_TYPE)

class Customer(Person):
    def save(self, *args, **kwargs):
        self.user_type = 'Customer'
        super().save(*args, **kwargs)


class Worker(Person):
    def save(self, *args, **kwargs):
        self.user_type = 'Worker'
        super().save(*args, **kwargs)


class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    subscribe_at = models.DateTimeField(default=timezone, null=False, blank=False)


class SubscriptionRecommendation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    recommendation_score = models.FloatField(default=0.0, null=False, blank=False)