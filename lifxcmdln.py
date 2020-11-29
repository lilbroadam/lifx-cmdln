import requests
import sys, getopt

tokenfile = None
args = {}
LIGHT_NAME = 'label'
POWER = 'power'
BRIGHTNESS = 'brightness'

def print_light_names(lightsJson):
    print('Your lights:')
    for i in range(len(lightsJson)):
        print(i, ': ', lightsJson[i].get(LIGHT_NAME), sep="")

def build_payload():
    payload = {}
    for i in args.keys():
        payload[i] = args.get(i)
    
    return payload

def main():
    global tokenfile
    if tokenfile is None:
        try:
            tokenfile = open("lifxtoken.txt", 'r')
        except FileNotFoundError:
            print('Error: unable to find token file.')
            exit(2)
    token = tokenfile.readline()

    response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))

    light_list = response.json()

    print_light_names(light_list)

    payload = build_payload()

    response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, auth=(token, ''))

if __name__=="__main__":

    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        arg = argv[i]

        if arg == '-power':
            if argv[i + 1] != 'on' and argv[i + 1] != 'off':
                print('Incorrect command line arguments')
                sys.exit(2)
            args[POWER] = argv[i + 1]
            i += 1
        elif arg == '-brightness':
            # TODO validate brightness param is (0, 1.0) 
            args[BRIGHTNESS] = argv[i + 1]
            i += 1
        elif arg == '--token-path':
            tokenfile = open(argv[i + 1], 'r')
            i += 1

        i += 1
        

    main()