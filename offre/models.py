from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class Media(models.Model):
    file = models.FileField(upload_to = "media/offer/", null=False, blank=False)
    upload_at = models.DateTimeField(null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = timezone.now()
        self.upload_at = current_date

        super().save(*args, **kwargs)

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

class Location(models.Model):
    country = models.CharField(null=False, blank=False, default="Cameroon", max_length=60)
    city = models.CharField(null=False, blank=False, max_length=100)
    locality = models.CharField(null=False, blank=False, max_length=255)

class WorkOffer(models.Model):
    STATUS = [("Open", "Open"),
              ("Close", "Close")]
    customer_owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    offer_title = models.CharField(blank=False, null=False, max_length=255)
    offer_description = models.TextField(blank=True, null=True)
    offer_price = models.FloatField(null=True, blank=True)
    offer_status = models.CharField(default="Open", max_length=20, choices=STATUS, null=False, blank=False)
    offer_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    post_at = models.DateTimeField(default=timezone.now(), blank=False, null=False)
    expire_date = models.DateField(null=True, blank=True)
    list_of_media = models.ManyToManyField(Media, blank=True)
    number_of_worker = models.IntegerField(null=True, blank=True)
    work_domain = models.CharField(max_length=255, null=False, blank=False, default='unknown')

class OfferApplication(models.Model):
    STATUS = [("Pending", "Pending"),
              ("Complete", "Complete"),
              ("Validated", "Validated")]
    worker_applicant = models.ForeignKey(Worker, on_delete=models.CASCADE)
    offer = models.ForeignKey(WorkOffer, on_delete=models.CASCADE)
    application_date = models.DateTimeField(default=timezone.now(), null=False, blank=False)
    attach_files = models.ManyToManyField(Media, null=True, blank=True)
    application_status = models.CharField(max_length=20, null=False, blank=False, choices=STATUS, default="Pending")

    def save(self, *args, **kwargs):
        if self.application_status == "Validated":
            # Nombre de candidatures déjà validées pour cette offre
            validated_count = OfferApplication.objects.filter(
                offer=self.offer,
                application_status="Validated"
            ).exclude(pk=self.pk).count()

            # Comparaison avec le nombre maximum de travailleurs
            if self.offer.number_of_worker is not None and validated_count >= self.offer.number_of_worker:
                raise ValidationError("Le nombre maximum de travailleurs pour cette offre a déjà été atteint.")
            elif self.offer.number_of_worker is not None and validated_count == self.offer.number_of_worker -1 :
                self.offer.offer_status = "Close"

        super().save(*args, **kwargs)

#Recommandations à gérer
class Recommender(models.Model):
    offer = models.ForeignKey(WorkOffer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    predict_recommendation = models.FloatField(null=False, blank=False)