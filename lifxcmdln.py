import requests

tokenfile = open("lifxtoken.txt", "r")
token = tokenfile.readline()

print(token)