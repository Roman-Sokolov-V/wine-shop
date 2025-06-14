from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

#User = get_user_model()

SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]


class Pet(models.Model):
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    breed = models.CharField(max_length=100, null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    coloration = models.CharField(max_length=50, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)])
    is_sterilized = models.BooleanField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, default=None)

    class Meta:
        verbose_name_plural = "pets"


    def __str__(self):
        return f"id {self.id}, a {self.type} named {self.name.capitalize()}"






