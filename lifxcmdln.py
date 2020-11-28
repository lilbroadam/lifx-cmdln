import requests

def print_light_names(lightsJson):
    LIGHT_NAME = 'label'

    print('Your lights:')
    for i in range(len(lightsJson)):
        print(i, ': ', lightsJson[i].get(LIGHT_NAME), sep="")

def main():
    tokenfile = open("lifxtoken.txt", "r")
    token = tokenfile.readline()

    response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))

    light_list = response.json()

    print_light_names(light_list)

if __name__=="__main__":
    main()