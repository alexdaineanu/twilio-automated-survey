from django.http import HttpResponse
from django_twilio.decorators import twilio_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from twilio.twiml.voice_response import VoiceResponse, Gather

from twilio_survey.models import Subscription
from twilio_survey.serializers import SubscriptionSerializer
from twilio_survey.tasks import send_sms, make_call


class ClientSubmitContactViewSet(GenericViewSet, CreateModelMixin):
	serializer_class = SubscriptionSerializer

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		make_call.apply_async(args=(response.data['id'],))
		return response


@twilio_view
def survey(request):
	sid = request.POST.get('CallSid')
	subscription = Subscription.objects.get(sid=sid)

	SURVEY_QUESTION = f'Hello {subscription.name}, whould you like to subscribe to updates from Alex? (Say Yes or No).'
	NO_INPUT_FALLBACK = 'We didn\'t receive any input. Goodbye!'
	HINTS = ['Yes', 'No']

	twilio_response = VoiceResponse()
	gather = Gather(input='speech', action='/twilio-survey/process-gather/', method='POST', hints=HINTS)
	gather.say(SURVEY_QUESTION)
	twilio_response.append(gather)
	twilio_response.say(NO_INPUT_FALLBACK)

	return twilio_response


@twilio_view
def process_gather(request):
	sid = request.POST.get('CallSid')

	AFIRMATIVE_RESPONSE = 'This is great! Welcome onboard.'
	NEGATIVE_RESPONSE = 'How unfortunate, maybe some other time.'

	response = VoiceResponse()

	data = request.POST
	result = data.get('SpeechResult')
	if 'yes' in result.lower():
		response.say(AFIRMATIVE_RESPONSE)
		Subscription.objects.filter(sid=sid).update(has_subscription=True)
	elif 'no' in result.lower():
		response.say(NEGATIVE_RESPONSE)

	return response


@twilio_view
def process_fallback(request):
	data = request.POST
	status = data.get('CallStatus')
	sid = data.get('CallSid')

	if status != 'completed':
		send_sms.apply_async(args=(sid, ))

	return HttpResponse(status=200)


@twilio_view
def leave_voicemail(request):
	MESSAGE = 'Hey, this is Alex trying to reach you!'

	data = request.POST
	status = data.POST.get('AnsweredBy')
	if status == 'machine_end_beep':
		response = VoiceResponse()
		response.say(MESSAGE)
		return response

	return HttpResponse(status=200)
