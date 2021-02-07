from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Subscription(TimeStampedModel):
	phone_number = PhoneNumberField(unique=True)
	name = models.CharField(max_length=255)
	sid = models.CharField(max_length=100, null=True)
	has_subscription = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.phone_number}'
