import requests

tokenfile = open("lifxtoken.txt", "r")
token = tokenfile.readline()

response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))

print(response)