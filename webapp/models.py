from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Author(models.Model):
    GenderType = models.TextChoices('GenderType', 'Male Female Others')
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=GenderType.choices)
    country = models.CharField(max_length=15)

class Books(models.Model):
    critic_validators = [MinValueValidator(limit_value=0), MaxValueValidator(limit_value=10)]
    name = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    number_of_pages = models.IntegerField()
    date_of_publishing = models.DateField()
    average_critics_rating = models.IntegerField(validators=critic_validators)
