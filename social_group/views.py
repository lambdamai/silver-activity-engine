from django.shortcuts import render
from django.template.response import TemplateResponse
from social_activity.forms import SocialGroup
# Create your views here.
def social_group(request):
    context = {}
    context['form'] = SocialGroup()
    return TemplateResponse(request, 'social_group.html', context)