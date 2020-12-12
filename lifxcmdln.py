import requests
import sys, getopt

from lifxutil import *

print_lights = False
tokenfile = None
cmdln_args = {} # rename to state_params

delta_params = {} # Parameters for the /state/delta API request


def main():
    token = read_token(tokenfile)

    if print_lights:
        # Get a list of the user's lights from /lights/:all
        response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))
        light_list = response.json()
        print_light_names(light_list)

    # Handle state params
    if len(cmdln_args) != 0:
        payload = build_state_payload(cmdln_args)

        # Send the /state API request with the pararmeters from the command line
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, auth=(token, ''))
        print_if_request_error(response)
    

    # Handle delta params
    # Send the /state API request with the pararmeters from the command line
    if len(delta_params) != 0:
        # payload = build_delta_payload(delta_params)
        payload = delta_params
        response = requests.post('https://api.lifx.com/v1/lights/all/state/delta', data=payload, auth=(token, ''))
        print_if_request_error(response)


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
            if argv[i][0] == '+':
                delta_params[BRIGHTNESS] = argv[i][1:] # Remove the + prefix
            elif argv[i][0] == '-':
                delta_params[BRIGHTNESS] = argv[i]
            else:
                cmdln_args[BRIGHTNESS] = argv[i]
        elif argv[i] == '-kelvin' or argv[i] == '-k' or argv[i] == '-temperature' or argv[i] == '-t':
            # TODO validate kelvin param is (1500, 9000)
            i += 1
            kelvin = argv[i]
            if kelvin[0] == '+':
                delta_params[KELVIN] = kelvin[1:] # Remove the + prefix
            elif kelvin[0] == '-':
                delta_params[KELVIN] = kelvin
            else:
                cmdln_args[KELVIN] = argv[i]
        elif argv[i] == '--list-lights':
            print_lights = True
        elif argv[i] == '--token-path':
            i += 1
            tokenfile = open(argv[i], 'r')

        i += 1

    main()