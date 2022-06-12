from django.test import TestCase
import requests


def pin_to_address(pin):
    address = requests.get('https://api.postalpincode.in/pincode/' + pin)
    
    return address.json()[0]['PostOffice'][0]['Name']


# Create your tests here.
print(pin_to_address('462041'))