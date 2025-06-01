from email.policy import default
from random import choices

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
        try:
            ip_address = get_ipaddress()
            location_data = get_location(ip_address)
            self.city = location_data["city"]
            self.country = location_data["country"]
            try :
                self.longitude = float(location_data["long"])

            except Exception as e:
                print(f"error : Ajout des donnees de la longitude ({location_data['long']}) échoué \n{e}")
                self.longitude = 0.0

            try :
                self.latitude = float(location_data["lat"])

            except Exception as e:
                print(f"error : Ajout des donnees de la latitude {location_data['lat']} échoué \n{e}")
                self.latitude = 0.0
        except Exception as e:
            self.city=""
            self.country=""
            self.longitude = 0.0
            self.latitude = 0.0

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
    end_date = models.DateField(null=True, blank=True)
    service = models.ForeignKey(ServicesProvided, on_delete=models.CASCADE)
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
    services = models.ManyToManyField(ServicesProvided, blank=True, null=True)
    experiences = models.ManyToManyField(Experience, blank=True, null=True)


#Retirer le status dans worker
#Creer une table evaluation des experience (worker, service et note evaluation)
#Faire un systeme de QCM genere par l'IA pour évaluer les aptitudes des workers (50 questions par service)
#Pour une évaluation on choisi aléatoirement 5
#Ajouter un compte a rebour de 30s par question

class MultipleQuestionAnswer(models.Model):
    question = models.TextField(blank = False, null=False)
    answer1 = models.TextField(blank = False, null=False)
    answer2 = models.TextField(blank = False, null=False)
    answer3 = models.TextField(blank = False, null=False)
    answer4 = models.TextField(blank = False, null=False)
    answer5 = models.TextField(blank = False, null=False)
    true_answer_id = models.IntegerField(blank=False, null=False)
    service = models.ForeignKey(ServicesProvided, on_delete=models.CASCADE)

class Evaluation(models.Model):
    STATUS = [("Unevaluated", "Unevaluated"),
              ("Beginner", "Beginner"),
              ("Intermediate", "Intermediate"),
              ("Confirmed", "Confirmed")]
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    service = models.ForeignKey(ServicesProvided, on_delete=models.CASCADE)
    final_marks = models.IntegerField(default=0)
    evaluation_status = models.CharField(choices=STATUS, max_length=20, blank=False, default= "Unevaluated")
    evaluate_at = models.DateTimeField(auto_now_add=True)


class EvaluationAnswer(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='worker_answers')
    question = models.ForeignKey(MultipleQuestionAnswer, on_delete=models.CASCADE)
    worker_answer_selection = models.IntegerField(blank=False, null=False)
