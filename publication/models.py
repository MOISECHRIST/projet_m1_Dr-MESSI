from django.db import models
from datetime import datetime

# Create your models here.

class Person(models.Model):
    LOGIN_STATUS = [("Logout", "Logout"),
                    ("Login", "Login")]
    id_person = models.IntegerField(unique=True, primary_key=True, blank=False, null=False)
    id_user = models.IntegerField(unique=True, blank=False, null=False)
    login_status = models.CharField(choices=LOGIN_STATUS, max_length=10, blank=False, null=False, default="Login")

    def save(self, *args, **kwargs):


        super().save(*args, **kwargs)

class Customer(Person):...

class Worker(Person):...

class Media(models.Model):
    file = models.FileField(upload_to = "media/publication/", null=False, blank=False)
    upload_at = models.DateTimeField(null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = datetime.now()
        self.upload_at = current_date

        super().save(*args, **kwargs)

class Publication(models.Model):
    text_publication = models.TextField()
    medias = models.ManyToManyField(Media, blank=True)
    post_at = models.DateTimeField(null=False, blank=False)
    update_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Worker, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = datetime.now()
        if self.modified:
           self.update_at = current_date
        else:
            self.post_at = current_date

        super().save(*args, **kwargs)



class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    text_comment = models.TextField()
    post_at = models.DateTimeField(default=datetime.now(), null=False, blank=False)
    update_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = datetime.now()
        if self.modified:
           self.update_at = current_date
        else:
            self.post_at = current_date

        super().save(*args, **kwargs)

class Like(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    post_at = models.DateTimeField(default=datetime.now(), null=False, blank=False)
    update_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = datetime.now()
        if self.modified:
            self.update_at = current_date
        else:
            self.post_at = current_date

        super().save(*args, **kwargs)


class Recommender(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    predict_preferences=models.FloatField(default=0.0, null=False, blank=False)