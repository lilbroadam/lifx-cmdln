DEFAULT_TOKEN_FILE = 'lifxtoken.txt'
LIGHT_NAME = 'label'
POWER = 'power'
BRIGHTNESS = 'brightness'
COLOR = 'color'
KELVIN = 'kelvin'

# Read and return the token in tokenfile.
# If tokenfile is None, read the token from DEFAULT_TOKEN_FILE
def read_token(tokenfile):
    if tokenfile is None:
        try:
            tokenfile = open(DEFAULT_TOKEN_FILE, 'r')
        except FileNotFoundError:
            print('Error: unable to find token file.')
            exit(2)
    return tokenfile.readline()

# Print the user's lights to the console
# lightsJson is the JSON returned by the /lights API request
def print_light_names(lightsJson):
    print('Your lights:')
    for i in range(len(lightsJson)):
        light = lightsJson[i]
        light_name = light.get(LIGHT_NAME)
        power = light.get(POWER)
        brightness = str(light.get(BRIGHTNESS)) + '%'
        color = light.get(COLOR)
        kelvin = str(color.get(KELVIN)) + 'K'
        light_formatted = '{0}: {1:<13} {2:<4} {3:<6} {4}'.format(i, light_name, power, brightness, kelvin)
        print(light_formatted, sep="")

# Format the JSON payload for the /state api request. This function
# is primarily for formatting the color parameter correctly.
# args is a dictionary of the state to be set (setting -> value)
def build_state_payload(args):
    payload = {}
    for i in args.keys():
        if i == KELVIN:
            color = KELVIN + ':' + args.get(i)
            payload[COLOR] = color
        # TODO elif HUE
        # TODO elif SATURATION
        else:
            payload[i] = args.get(i)

    return payload

# Print the HTML status code if there was an error with the request
def print_if_request_error(response):
    status_code = response.status_code
    if status_code != 200 and status_code != 207:
        print('HTML request error', response.status_code)
        print(response.text) # TODO Add a -debug flag to print this
