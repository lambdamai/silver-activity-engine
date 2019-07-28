from django.shortcuts import render
from django.template.response import TemplateResponse
# Create your views here.
from .forms import ActivityForm
import requests

from requests import get, Session, adapters
from instagram_private_api import Client, ClientCompatPatch
user_name = ''
password = ''
api = Client(user_name, password)

"""
https://api.instagram.com/oauth/authorize/?client_id=118e8d13dda245648519242b7508feb0&redirect_uri=https://elfsight.com/service/generate-instagram-access-token/&response_type=code&scope=public_content
"""
import vk_api

vk_session = vk_api.VkApi('', '')
vk_session.auth()
vk = vk_session.get_api()


def getVKPosts(latitude, longitude, text):
    posts = vk.newsfeed.search(q=text, latitude=latitude, longitude=longitude)
    children = []
    for post in posts['items']:
        children.append(post['text'])
        print(text, post['text'])
    list_post = {'location': (latitude, longitude), 'name':text, 'children': children}

    return list_post

def getInstaPosts(latitude, longitude, name_company, count):
    list_address_company = []
    results = api.location_search(latitude, longitude)
    for loc in results['venues'][:30]:
        if len(str(loc['lat'])) > 8 and len(str(loc['lng'])) > 8:
            print("Original", name_company)
            print("Find", loc['name'])
            print(latitude, longitude)
            print("Address", loc['address'])
            child = []
            posts = api.location_section(loc['external_id'], api.generate_uuid(), 'ranked')
            print(len(posts['sections']))
            for post in posts['sections']:
                try:
                    child.append(post['layout_content']['medias'][0]['media']['caption']['text'])
                except:
                    pass
            list_address_company.append({'location': (loc['lat'], loc['lng']), 'name': loc['name'],
                                         'children': child, 'average_sentimental':0})
    return list_address_company


def index(request):
    context = {}
    return TemplateResponse(request, "main.html", context={})


def activity_map(request):
    context = {'form': ActivityForm()}
    if request.POST:
        form = ActivityForm(request.POST)
        if form.is_valid():
            app_id = 'k3AV3uCmGiomemHkMc6u'
            app_code = '4VHf_IBXVgvh0ncmD98XEg'
            lat = form['lat'].value()
            lng = form['lng'].value()
            cat = form['category'].value()
            url = f'https://places.cit.api.here.com/places/v1/discover/explore?in={lat}%2C{lng}%3Br%3D300.0&cat={cat}&Accept-Language=ru-RU%2Cru%3Bq%3D0.9%2Cen-US%3Bq%3D0.8%2Cen%3Bq%3D0.7&app_id={app_id}&app_code={app_code}'
            resp = requests.get(url=url)
            results = []
            data = resp.json()  # Check the JSON Response Content documentation below
            for item in data['results']['items']:
                vk_post = getVKPosts(item['position'][0], item['position'][1], item['title'])
                print(vk_post)
                #insta_post = getInstaPosts(item['position'][0], item['position'][1], item['title'], 90)
                #results.append(insta_post)
            #print(results)
    return TemplateResponse(request, "activity_form.html", context)
