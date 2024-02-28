from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User




class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, null=True,blank=True)
    boarding =models.CharField(max_length=250, null=True,blank=True)
    destination =models.CharField(max_length=250, null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Package(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, null=True,blank=True)
    boarding =models.CharField(max_length=250, null=True,blank=True)
    destination =models.CharField(max_length=250, null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=250, null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.value
    

class CustomerEnqiuery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, null=True,blank=True)
    destination = models.CharField(max_length=250, null=True,blank=True)
    date_of_travel = models.DateField(null=True,blank=True)
    phone_number = models.IntegerField(null=True,blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True,blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True,blank=True)
    accepted = models.CharField(max_length=250, null=True,blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class CustomerDetails(models.Model):
    customerenqid = models.ForeignKey(CustomerEnqiuery, on_delete=models.CASCADE, null=True,blank=True)
    borading = models.CharField(max_length=250, null=True,blank=True)
    destination = models.CharField(max_length=250, null=True,blank=True)
    date = models.DateField( null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Passenger(models.Model):
    customerdetailsid = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True,blank=True)    
    name = models.CharField(max_length=250, null=True,blank=True)
    age = models.CharField(max_length=250, null=True,blank=True)
    gender = models.CharField(max_length=250, null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
class PassengerDoc(models.Model):
    customerdetailsid = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True,blank=True)      
    name = models.CharField(max_length=250, null=True,blank=True)
    id_type = models.CharField(max_length=250, null=True,blank=True)
    upload_documents = models.FileField(blank=True,
                                        upload_to='Customer Documents/%Y/%m/%d', max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)