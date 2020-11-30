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
        print(i, ': ', lightsJson[i].get(LIGHT_NAME), sep="")

# Format the JSON payload for the /state api request
# args is a dictionary of the state to be set (setting -> value)
def build_payload(args):
    payload = {}
    for i in args.keys():
        if i == KELVIN:
            color = KELVIN + ':' + args.get(i)
            payload[COLOR] = color
        else:
            payload[i] = args.get(i)

    return payload