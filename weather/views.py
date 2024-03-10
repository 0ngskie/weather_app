from django.shortcuts import render
import requests
# Forms
from . forms import CityForm


# requests
from . requests import current_weather

def get_weather(request):
    
    payload = {
        'key' :'29226d76946a46d98c915428240502'
    }

    url = 'http://api.weatherapi.com/v1/current.json'

    response = requests.get(url, params = payload)

    print(response.status_code)
    print(response.url)

    return response.json()

# Create your views here.
def weather(request):

    api_response = get_weather(request)

    print(api_response)

    context = {
        'response': api_response
    }
    return render(request, 'weather/base.html', context = context)




def home(request):
    '''
        accept and handle user input using forms.py in this case we created CityForm
    	we make requests using the requests.py
        see base.html in the templates folder.

    '''
    
    api_response = {}
    
    if request.method == 'POST':
        city_input = CityForm(request.POST) # from /forms.py
        
        if city_input.is_valid():
            city_name = city_input.cleaned_data['city_input'].lower().split()
            api_response = current_weather(request, city_name=city_name) # STORE API response
            
            print(api_response)
            print(city_name)   
            
            
            
            if 'error' in api_response:
                # This handles if a user tries to input a non existing city or an invalid input.
                error_message = api_response['error']['message']
                api_response = {'error': f"Error fetching data: {error_message}"}
                print(api_response)
    
    else:
        city_input = CityForm()          
    
    
    context = {
        'city_input': city_input,
        'response': api_response
    }
    
    return render(request, 'weather/base.html', context=context )