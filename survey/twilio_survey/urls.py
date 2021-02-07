from django.urls import path

from . import api_views
from .api_views import survey, process_gather, process_fallback

urlpatterns = [
    path('submit-contact/', api_views.ClientSubmitContactViewSet.as_view({'post': 'create'}), name='submit_contact'),
    path('survey/', survey, name='survey'),
    path('process-gather/', process_gather, name='process_gather'),
    path('process-fallback/', process_fallback, name='process_fallback')
]
