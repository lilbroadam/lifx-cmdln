import requests
import sys, getopt

from lifxutil import *

print_lights = False
tokenfile = None
args = {}

def main():
    token = read_token(tokenfile)

    if print_lights:
        response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))
        light_list = response.json()
        print_light_names(light_list)

    payload = build_payload(args)

    response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, auth=(token, ''))

if __name__=="__main__":
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] == '-power' or argv[i] == '-p':
            if argv[i + 1] != 'on' and argv[i + 1] != 'off':
                print('Incorrect command line arguments')
                sys.exit(2)
            args[POWER] = argv[i + 1]
            i += 1
        elif argv[i] == '-brightness' or argv[i] == '-b':
            # TODO validate brightness param is (0, 1.0) 
            args[BRIGHTNESS] = argv[i + 1]
            i += 1
        elif argv[i] == '--list-lights':
            print_lights = True
        elif argv[i] == '--token-path':
            tokenfile = open(argv[i + 1], 'r')
            i += 1

        i += 1

    main()