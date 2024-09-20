from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=15)

class Registration(models.Model):
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    house=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class Doctor(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    

class Pharmacist(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    

class Booking(models.Model):
    bookeddate=models.DateField(auto_now_add=True,null=True)
    token=models.IntegerField(null=True, blank=True)
    regid=models.ForeignKey(Registration,on_delete=models.CASCADE)
    docid=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    bookingdate=models.DateField()
    status=models.CharField(max_length=100)

class Payment(models.Model):
    bid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    paydate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=50)

class Medicine(models.Model):
    name=models.CharField(max_length=100)
    desc = models.CharField(max_length=100,null=True)
    rate=models.CharField(max_length=10,null=True)
    status=models.CharField(max_length=10,null=True,default='Available')

class Prescription(models.Model):
    bid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    diagnosis=models.CharField(max_length=100)    

class PresMedicine(models.Model):
    prescription=models.ForeignKey(Prescription,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    desc = models.CharField(max_length=100,null=True)
    qty=models.IntegerField()
    status=models.CharField(max_length=10,null=True,default='Prescribed')

    

