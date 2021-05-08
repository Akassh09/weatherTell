from django.shortcuts import render
from selenium import webdriver
from django.conf import settings
import os

driver = webdriver.Chrome(executable_path=os.path.join(settings.BASE_DIR,'chromedriver_win32/chromedriver.exe'))

def get_html_content(request):

    city = request.GET.get('city')
    city = city.replace(" ", "+")
    html_content = driver.get(f'https://www.google.com/search?q=weather+{city}')
    return html_content


def index(request):
    city_weather = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        
        # extract region
        city_name = driver.find_element_by_id("wob_loc")
        city = city_name.text
        # extract temperature now
        temp = driver.find_element_by_id("wob_tm")
        temp = temp.text
        # get the day and hour now
        daytime = driver.find_element_by_id("wob_dts")
        daytime = daytime.text
        # get the actual weather
        desc = driver.find_element_by_id("wob_dc")
        desc = desc.text

        image = driver.find_element_by_id("wob_tci")
        img = image.get_attribute('src')

        city_weather = {
           'city': city,
            'temp': temp,
            'dayhour' : daytime,
            'desc': desc,
            'img': img,
        }

    return render(request, 'index.html', {'weather': city_weather})

