from django.db import models


SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]


class Pet(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    breed = models.CharField(max_length=100, null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    coloration = models.CharField(max_length=50, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    is_sterilized = models.BooleanField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "pets"

    def __str__(self):
        return f"id {self.id}, a {self.type} named {self.name.capitalize()}"




