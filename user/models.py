from django.db import models
from django.contrib.auth.models import User
from .ip_location import get_location, get_ipaddress

#Person
    #profile_image = image (facultative)
    #date_of_birth = Date
    #gender = chooses
    #phone_number = str (facultative)
    #long = float
    #lat = float
    #city = str
    #country = str
    #user -> User(firstname, lastname, email, username, password)
class Person(models.Model):
    GENDER = [("Female", "Female"),
              ("Male", "Male")]

    profile_image = models.ImageField(upload_to="media/profile/", null=True, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(choices=GENDER, max_length=100, blank=False, null=False)
    phone_number = models.CharField(blank=True, null=True, max_length=150)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    city = models.CharField(blank=True, null = True, max_length=150)
    country = models.CharField(blank=True, null = True, max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Si l'objet est nouveau, on récupère l'IP et la localisation
        if not self.pk:
            ip_address = get_ip_address()
            location_data = get_location(ip_address)
            self.city = location_data.get("city", "")
            self.country = location_data.get("country", "")
            self.longitude = location_data.get("longitude", 0.0)
            self.latitude = location_data.get("latitude", 0.0)

        super().save(*args, **kwargs)



#ServicesProvided
    #service_name = str
    #service_description = text (facultative)
class ServicesProvided(models.Model):
    service_name = models.CharField(blank=False, null=False, max_length=250)
    service_description = models.TextField(blank=True, null=True)

#PreferenceArea
    #service -> ServicesProvided
    #person -> Personne
class PreferenceArea(models.Model):
    service = models.ForeignKey(ServicesProvided, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


#Customer
    #person -> Person(...)
class Customer(Person):
    pass

#Experience
    #employer_name = str
    #employer_phone = str
    #employer_email = str
    #start_date = Date
    #end_date = Date (facultative)
    #experience_description = text (facultative)
class Experience(models.Model):
    employer_name = models.CharField(blank=False, null=False, max_length=255)
    employer_phone = models.CharField(blank=False, null=False, max_length=255)
    employer_email = models.EmailField(max_length=255)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    experience_description = models.TextField(blank=True, null=True)

#Worker
    #person -> Person(...)
    #headline = text
    #about_worker = text (facultative)
    #cover_image = image
    #services -> list(ServicesProvided)
    #experiences -> List(Experience)
class Worker(Person):
    headline = models.TextField(null=False, blank=True)
    about_worker = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="media/cover_image/", null=True, blank=True)
    services = models.ManyToManyField(ServicesProvided)
    experiences = models.ManyToManyField(Experience)