from django.db import models
from django.contrib.auth.models import User

#Person
    #profile_image = image
    #date_of_birth = Date (facultative)
    #gender = chooses (facultative)
    #phone_number = str (facultative)
    #long = float
    #lat = float
    #city = str
    #country = str
    #user -> User(firstname, lastname, email, username, password)

#ServicesProvided
    #service_name = str
    #service_description = text (facultative)

#PeferenceArea
    #service -> ServicesProvided
    #person -> Personne

#Customer
    #person -> Person(...)

#Experience
    #employer_name = text
    #employer_phone = str
    #employer_email = str
    #start_date = Date
    #end_date = Date (facultative)
    #experience_description = text (facultative)

#Worker
    #person -> Person(...)
    #headline = text
    #about_worker = text (facultative)
    #cover_image = image
    #services -> list(ServicesProvided)
    #experiences -> List(Experience)
    #list_training -> List(Training)

