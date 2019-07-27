from django.shortcuts import render
from django.template.response import TemplateResponse
# Create your views here.
from  .forms import ActivityForm
import requests

from requests import get, Session, adapters


"""
https://api.instagram.com/oauth/authorize/?client_id=118e8d13dda245648519242b7508feb0&redirect_uri=https://elfsight.com/service/generate-instagram-access-token/&response_type=code&scope=public_content
"""
def getInstaPosts(latitude, longitude, distance, count):
    from instagram_private_api import Client, ClientCompatPatch

    user_name = ''
    password = ''

    api = Client(user_name, password)
    results = api.location_search(latitude, longitude)
    print(results)
    for loc in results['venues'][1:3]:
        if len(str(loc['lat'])) > 7 and len(str(loc['lng'])) > 7:
            print("Id", loc['external_id'])

            posts = api.location_section(loc['external_id'], api.generate_uuid(), 'recent' )
            for post in posts['sections'][:15]:
                
            print()
            print("Address",loc['address'])
            print("Name",loc['name'])
            print("lat", loc['lat'])
            print("lng", loc['lng'])
            print()


def index(request):
    context = {}
    return TemplateResponse( request, "main.html", context={})


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
            data = resp.json()  # Check the JSON Response Content documentation below
            for item in data['results']['items']:
                print(item['position'])
                print(item['title'])
                print(item['category']['title'])
                print()
            insta_post = getInstaPosts(lat, lng, 300, 90)


    return TemplateResponse( request, "activity_form.html", context)

