from rest_framework import serializers

from twilio_survey.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'phone_number', 'name')
