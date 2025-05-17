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

class Media(models.Model):
    file = models.FileField(upload_to = "media/publication/", null=False, blank=False)
    upload_at = models.DateTimeField(null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = timezone.now()
        self.upload_at = current_date

        super().save(*args, **kwargs)

class Publication(models.Model):
    text_publication = models.TextField()
    medias = models.ManyToManyField(Media, blank=True)
    post_at = models.DateTimeField(default= timezone.now() ,null=False, blank=False)
    update_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Worker, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = timezone.now()
        if self.modified:
           self.update_at = current_date
        else:
            self.post_at = current_date

        super().save(*args, **kwargs)



class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    text_comment = models.TextField()
    post_at = models.DateTimeField(default=timezone.now(), null=False, blank=False)
    update_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, null=False, blank=False)

    def save(self, *args, **kwargs):
        current_date = timezone.now()
        if self.modified:
           self.update_at = current_date
        else:
            self.post_at = current_date

        super().save(*args, **kwargs)

class Like(models.Model):
    LIKE_VALUE = [("Like", "Like"),
                  ("Neutral", "Neutral"),
                  ("Hate","Hate")]
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    post_at = models.DateTimeField(default=timezone.now(), null=False, blank=False)
    update_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, null=False, blank=False)
    like_value = models.CharField(default="Neutral", choices=LIKE_VALUE, max_length=20, blank=False, null=False)


    def save(self, *args, **kwargs):
        current_date = timezone.now()
        if self.modified:
            self.update_at = current_date
        else:
            self.post_at = current_date

        super().save(*args, **kwargs)

class Screen_Print(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    viewer = models.ForeignKey(Person, on_delete=models.CASCADE)
    view_at = models.DateTimeField(default=timezone.now(), null=False, blank=False)


class Recommender(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    predict_preferences=models.FloatField(default=0.0, null=False, blank=False)