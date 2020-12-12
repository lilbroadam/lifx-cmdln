import requests
import sys, getopt

from lifxutil import *

print_lights = False
tokenfile = None
state_params = {} # Parameters for the /state API request
delta_params = {} # Parameters for the /delta API request


def main():
    token = read_token(tokenfile)

    # Print the user's lights form /lights/:all
    if print_lights:
        response = requests.get('https://api.lifx.com/v1/lights/all', auth=(token, ''))
        light_list = response.json()
        print_light_names(light_list)

    # Send the /state API request with the pararmeters from the command line
    if len(state_params) != 0:
        payload = build_state_payload(state_params)
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, auth=(token, ''))
        print_if_request_error(response)

    # Send the /delta API request with the pararmeters from the command line
    if len(delta_params) != 0:
        response = requests.post('https://api.lifx.com/v1/lights/all/state/delta', data=delta_params, auth=(token, ''))
        print_if_request_error(response)


if __name__=="__main__":
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] == '-power' or argv[i] == '-p':
            i += 1
            if argv[i] != 'on' and argv[i] != 'off':
                print('Incorrect command line arguments')
                sys.exit(2)
            state_params[POWER] = argv[i]
        elif argv[i] == '-brightness' or argv[i] == '-b':
            # TODO validate brightness param is (0, 1.0) 
            i += 1
            brightness = argv[i]
            if brightness[0] == '+':
                delta_params[BRIGHTNESS] = brightness[1:] # Remove the + prefix
            elif brightness[0] == '-':
                delta_params[BRIGHTNESS] = brightness
            else:
                state_params[BRIGHTNESS] = brightness
        elif argv[i] == '-kelvin' or argv[i] == '-k' or argv[i] == '-temperature' or argv[i] == '-t':
            # TODO validate kelvin param is (1500, 9000)
            i += 1
            kelvin = argv[i]
            if kelvin[0] == '+':
                delta_params[KELVIN] = kelvin[1:] # Remove the + prefix
            elif kelvin[0] == '-':
                delta_params[KELVIN] = kelvin
            else:
                state_params[KELVIN] = kelvin
        elif argv[i] == '--list-lights' or argv[i] == '--show':
            print_lights = True
        elif argv[i] == '--token-path':
            i += 1
            tokenfile = open(argv[i], 'r') # TODO handle if file not found

        i += 1

    main()