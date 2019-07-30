from django.shortcuts import render
from django.template.response import TemplateResponse
# Create your views here.
from .forms import ActivityForm
import requests

from requests import get, Session, adapters
from instagram_private_api import Client, ClientCompatPatch
user_name = '' # INSTAGRAM LOGIN
password = '' # INSTAGRAM PASSWORD
api = Client(user_name, password)
import random
import vk_api
import math
import numpy as np

vk_session = vk_api.VkApi('', '') # VK LOGIN PASSWORD
vk_session.auth()
vk = vk_session.get_api()


def getVKPosts(latitude, longitude, text):
    posts = vk.newsfeed.search(q=text, latitude=latitude, longitude=longitude)
    children = []
    for post in posts['items']:
        children.append(post['text'])
        print(text, post['text'])
    list_post = {'location': (latitude, longitude), 'name':text, 'children': children}
    for x in list_post['children']:
        print(x)
    return list_post

def getInstaPosts(latitude, longitude, name_company, count):
    list_address_company = []
    results = api.location_search(latitude, longitude)
    for loc in results['venues'][1:10]:
        if len(str(loc['lat'])) > 8 and len(str(loc['lng'])) > 8:
            print("Original", name_company)
            print("Find", loc['name'])
            print(latitude, longitude)
            print("Address", loc['address'])
            child = []
            posts = api.location_section(loc['external_id'], api.generate_uuid(), 'ranked')
            print(len(posts['sections']))
            for post in posts['sections'][:15]:
                try:
                    child.append(post['layout_content']['medias'][0]['media']['caption']['text'])
                except:
                    pass

            list_address_company.append({'location': (loc['lat'], loc['lng']), 'name': loc['name'],
                                         'children': child})
    result_list = []
    for item in list_address_company:
        result_list.append({'lat':item['location'][0], 'lng':item['location'][1], 'volume': random.random()})

    return result_list


def index(request):
    context = {}
    return TemplateResponse(request, "main.html", context={})


def activity_map(request):
    context = {'form': ActivityForm()}
    if request.POST:
        form = ActivityForm(request.POST)
        if form.is_valid():

            app_id = '' # HERE APP ID
            app_code = '' #HERE APP CODE
            lat = form['lat'].value()
            lng = form['lng'].value()
            cat = form['category'].value()
            url = f'https://places.cit.api.here.com/places/v1/discover/explore?in={lat}%2C{lng}%3Br%3D300.0&cat={cat}&Accept-Language=ru-RU%2Cru%3Bq%3D0.9%2Cen-US%3Bq%3D0.8%2Cen%3Bq%3D0.7&app_id={app_id}&app_code={app_code}'
            resp = requests.get(url=url)
            results = []
            shops = []
            context['agenda_place'] = {'lat': lat, 'lng': lng, 'name':"Точка аренды"}
            data = resp.json()  # Check the JSON Response Content documentation below
            for item in data['results']['items']:
                shops.append({'lat': item['position'][0], 'lng':item['position'][1], 'name':item['title']})
                #vk_post = getVKPosts(item['position'][0], item['position'][1], item['title'])
                #print(vk_post)
                insta_post = getInstaPosts(item['position'][0], item['position'][1], item['title'], 90)
                results.extend(insta_post) # получаем посты от инстаграмма

            predict = huff(shops, results)
            context['predict'] = predict
            context['shops'] = shops
            context['results'] = results
            print(shops)
            print(results)
            return TemplateResponse(request, "activity_map.html", context)
            #print(results)
    return TemplateResponse(request, "main.html", context)


def huff(A, B):
    A = [{'lat': float(a['lat']), 'lng': float(a['lng']), 'volume': float(a['volume'])} for a in A]
    B = [{'lat': float(a['lat']), 'lng': float(a['lng']), 'volume': float(a['volume'])} for a in B]

    def d(x_1, x_2, y_1, y_2):
        return math.hypot(x_1 - x_2, y_1 - y_2)

    for a in A:
        a['volume'] = 0

    while B:
        b = B.pop()
        D = [d(a['lat'], b['lat'], a['lng'], b['lng']) for a in A]
        A[D.index(min(D))]['volume'] += b['volume']

    points = [(a['lat'], a['lng'], a['volume']) for a in A]

    lat_min = min(points, key=lambda x: x[0])[0]
    lng_min = min(points, key=lambda x: x[1])[1]
    lat_d = max(points, key=lambda x: x[0])[0] - lat_min
    lng_d = max(points, key=lambda x: x[1])[1] - lng_min

    points = [((p[0] - lat_min) / lat_d, (p[1] - lng_min) / lng_d, p[2]) for p in points]

    data = []
    for _ in points:
        data.append({})

    for (i, (x_t, y_t, s_t)) in enumerate(points):
        for y in np.arange(-0.2, 1.2, 0.05):
            for x in np.arange(-0.2, 1.2, 0.05):
                data[i][x, y] = (s_t / d(x_t, x, y_t, y)) / sum(s1 / d(x, x1, y, y1) for (y1, x1, s1) in points)
    ret = []
    for e in data:
        ret.append(sum(e.values()))
    return ret

def social_network(request):
    pass
