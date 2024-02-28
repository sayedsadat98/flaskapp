# models.py

from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.apps import apps

class UserPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_choices = [
        ('basic', 'Basic Plan'),
        ('standard', 'Standard Plan'),
        ('premium', 'Premium Plan'),
    ]
    plan_type = models.CharField(max_length=10, choices=plan_choices)
    plan_price = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set expiration_date to purchase_date + 30 days
        if not self.expiration_date:
            self.expiration_date = self.purchase_date + timedelta(days=30)
        super(UserPlan, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan_type} - {self.plan_price} USD - Expires: {self.expiration_date}"

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserServiceLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    limit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.limit} requests"

# If you need to track API requests made by users, you can create a model for that as well
class ApiRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.timestamp}"

 

class Emails(models.Model):
    subject = models.CharField(max_length=500)
    message = models.TextField(max_length=500)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):

        # Call the original save method
        super().save(*args, **kwargs)


        # Send email when a new entry is saved
        my_subject = self.subject
        plain_message = self.message
        my_recipient = self.email

        # Create and send EmailMultiAlternatives
        message = EmailMultiAlternatives(
            subject=my_subject,
            body=plain_message,
            from_email=None,
            to=[my_recipient],
        )

        message.send()
    