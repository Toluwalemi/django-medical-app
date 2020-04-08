from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Admin:
        pass


class Practitioner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Admin:
        pass


class Illness(models.Model):
    name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "illnesses"

    def __str__(self):
        return self.name


class MedicalInfo(models.Model):
    summary = models.CharField(max_length=256)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    illnesses = models.ManyToManyField(Illness)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Medical Information"

    def get_illness(self):
        return ",".join([str(p) for p in self.illnesses.all()])

    def __str__(self):
        return self.summary
