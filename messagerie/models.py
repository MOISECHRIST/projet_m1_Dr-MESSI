from django.db import models
from django.utils import timezone


# Create your models here.
class Media(models.Model):
    file = models.FileField(upload_to = "media/messages/", null=False, blank=False)
    upload_at = models.DateTimeField(null=False, blank=False, auto_now=True)

    def save(self, *args, **kwargs):
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


#Conversation
#   participants -> list(Person)
#   update_at -> datetime
class Conversation(models.Model):
    participants = models.ManyToManyField(Person)
    update_date =  models.DateTimeField(auto_now=True)

#Message
#   conversation -> Conversation
#   sender -> Person
#   created_at -> datetime
#   text_message -> Text
#   medias -> list(Media) or blank
#   is_read -> boolean
#   read_at -> datetime or blank
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    is_received = models.BooleanField(default=False)
    received_at = models.DateTimeField(blank=True, null=True)

    def message_read(self):
        self.is_read=True
        self.read_at = timezone.now()
        self.save()

    def message_received(self):
        participants = self.conversation.participants.all()
        recipients = [p for p in participants if p != self.sender]
        for recipient in recipients:
            if recipient.login_status == "Login":
                self.is_received = True
                self.received_at = timezone.now()
                self.save()
                break


