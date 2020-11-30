import requests
import sys, getopt

from lifxutil import *

print_lights = False
tokenfile = None
cmdln_args = {}

def main():
    token = read_token(tokenfile)

    if print_lights:
        # Get a list of the user's lights from /lights/:all
        response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))
        light_list = response.json()
        print_light_names(light_list)

    payload = build_payload(cmdln_args)

    # Send the /state API request with the pararmeters from the command line
    response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, auth=(token, ''))

    # Print the HTML status code if there was an error with the request
    status_code = response.status_code
    if status_code != 200 and status_code != 207:
        print('HTML request error', response.status_code)

if __name__=="__main__":
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] == '-power' or argv[i] == '-p':
            if argv[i + 1] != 'on' and argv[i + 1] != 'off':
                print('Incorrect command line arguments')
                sys.exit(2)
            i += 1
            cmdln_args[POWER] = argv[i]
        elif argv[i] == '-brightness' or argv[i] == '-b':
            # TODO validate brightness param is (0, 1.0) 
            i += 1
            cmdln_args[BRIGHTNESS] = argv[i]
        elif argv[i] == '-kelvin' or argv[i] == '-k' or argv[i] == '-temperature' or argv[i] == '-t':
            # TODO validate kelvin param is (1500, 9000)
            i += 1
            cmdln_args[KELVIN] = argv[i]
        elif argv[i] == '--list-lights':
            print_lights = True
        elif argv[i] == '--token-path':
            i += 1
            tokenfile = open(argv[i], 'r')

        i += 1

    main()