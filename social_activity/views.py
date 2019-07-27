from django.shortcuts import render
from django.template.response import TemplateResponse
# Create your views here.
from  .forms import ActivityForm
import requests

from requests import get, Session, adapters

def getInstaPosts(latitude, longitude, distance, count):
    params = {
        'lat': latitude,
        'lng': longitude,
        'distance': distance, # radius of requested area
        'count': count, # number of posts(100 max)
        'access_token': '37433013.118e8d1.13687b6c616946b6b8629f15fdc82696' #your access token
    }
    session = Session()
    session.mount("https://", adapters.HTTPAdapter(max_retries=10))

    response = session.get("https://api.instagram.com/v1/media/search", params=params, verify=True)

    return response.json()


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
            print(insta_post)


    return TemplateResponse( request, "activity_form.html", context)

