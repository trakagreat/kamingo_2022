from django.test import TestCase
import requests


def pin_to_address(pin):
    address = requests.get('https://api.postalpincode.in/pincode/' + pin)
    return address.json()

