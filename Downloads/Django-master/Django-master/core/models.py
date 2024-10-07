from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
   
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)  
    celular = models.CharField(max_length=15) 
    date = models.DateField()
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.nome

class Login(models.Model):
    email = models.EmailField(max_length=254)
    cpf = models.CharField(max_length=11)

@receiver(post_save, sender=Usuario)
def create_login(sender, instance, created, **kwargs):
    if created:
        Login.objects.create(email=instance.email, cpf=instance.cpf)