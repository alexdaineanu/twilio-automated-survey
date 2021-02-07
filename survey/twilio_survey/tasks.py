from urllib.parse import urljoin

from celery import shared_task
from django.conf import settings

from twilio_survey import client
from twilio_survey.models import Subscription


@shared_task()
def make_call(subscription_id):
	subscription = Subscription.objects.get(id=subscription_id)
	phone_number = subscription.phone_number
	url = urljoin(settings.NGROK_URL, 'twilio-survey/survey/')
	status_callback_url = urljoin(settings.NGROK_URL, 'twilio-survey/process-fallback/')

	response = client.calls.create(
		url=url,
		to=phone_number.raw_input,
		from_=settings.TWILIO_PHONE_NUMBER,
		status_callback=status_callback_url,
		machine_detection='DetectMessageEnd',
	)
	Subscription.objects.filter(id=subscription_id).update(sid=response.sid)


@shared_task()
def send_sms(sid):
	subscription = Subscription.objects.get(sid=sid)
	MESSAGE = f'Hi {subscription.name}, this is Alex. Let me know when is a better time to chat.'

	client.messages.create(to=subscription.phone_number.raw_input, from_=settings.TWILIO_PHONE_NUMBER, body=MESSAGE)
