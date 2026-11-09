from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Student(models.Model):
    COURSE_CHOICES = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('MATH', 'Mathematics'),
        ('PHY', 'Physics'),
        ('BIO', 'Biology'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField(validators=[MinValueValidator(1)])
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('students:detail', args=[self.pk])
