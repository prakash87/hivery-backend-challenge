"""
Models for the application
"""
import datetime

import django.db.models as models


class Company(models.Model):
    """
    Stores data imported from companies.json file
    """
    # -- Field to help with data import --
    index_with_prefix = models.CharField(max_length=50, null=True)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    """
    Stores the processed data imported from people.json file
    """
    TYPE_FRUIT = 'F'
    TYPE_VEGETABLE = 'V'
    TYPE_OTHER = 'O'

    TYPE_CHOICES = (
        (TYPE_FRUIT, 'Fruit'),
        (TYPE_VEGETABLE, 'Vegetable'),
        (TYPE_OTHER, 'Other'),
    )

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True)

    def __str__(self):
        return self.name


class PersonTag(models.Model):
    """
    Stores the processed data imported from people.json file
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    """
    Stores data imported from people.json file.
    Some fields have been modified to keep the data clean.
    greeting - this field is not included as it doesn't have any meaningful information on it's own.
    friends - this field is renamed to 'following' as a 'friend' of A might not have A in his/her friend list.
    age - this field is renamed to 'year_of_birth' as the age is increased every year.
    has_died - this field is renamed to 'is_alive' to avoid double negative in logic. Value is toggled before saving.
    """
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'

    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other')
    )

    EYE_COLOR_ALBINO = 'AL'
    EYE_COLOR_BLUE = 'BL'
    EYE_COLOR_BROWN = 'BR'
    EYE_COLOR_GREEN = 'GR'
    EYE_COLOR_GREY = 'GY'
    EYE_COLOR_HAZEL = 'HZ'
    EYE_COLOR_OTHER = 'OT'

    EYE_COLOR_CHOICES = (
        (EYE_COLOR_ALBINO, 'Albino'),
        (EYE_COLOR_BLUE, 'Blue'),
        (EYE_COLOR_BROWN, 'Brown'),
        (EYE_COLOR_GREEN, 'Green'),
        (EYE_COLOR_GREY, 'Grey'),
        (EYE_COLOR_HAZEL, 'Hazel'),
        (EYE_COLOR_OTHER, 'Other'),

    )

    # --- ids from previous system ---
    old_id = models.CharField(max_length=100, null=True)
    guid = models.CharField(max_length=100, null=True)

    # -- Field to help with data import --
    index_with_prefix = models.CharField(max_length=50, null=True)

    # --- Identity ---
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    year_of_birth = models.PositiveIntegerField()
    eye_color = models.CharField(max_length=2, choices=EYE_COLOR_CHOICES)

    # --- Contact details ---
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    # --- Work ---
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.SET_NULL, null=True)

    # --- Profile ---
    about = models.TextField()
    picture_url = models.URLField()
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    favorite_foods = models.ManyToManyField(Food, related_name='people')

    # --- Miscellaneous ---
    tags = models.ManyToManyField(PersonTag, related_name='people')
    registration_date = models.DateTimeField()
    is_alive = models.BooleanField()

    # Better to move this field to 'Transaction' or similar model in future
    balance = models.CharField(max_length=50, help_text='Balance in dollars')

    def __str__(self):
        return self.name

    def get_age(self):
        return datetime.datetime.today().year - self.year_of_birth