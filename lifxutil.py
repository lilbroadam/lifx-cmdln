LIGHT_NAME = 'label'
POWER = 'power'
BRIGHTNESS = 'brightness'
COLOR = 'color'
KELVIN = 'kelvin'

def read_token(tokenfile):
    if tokenfile is None:
        try:
            tokenfile = open("lifxtoken.txt", 'r')
        except FileNotFoundError:
            print('Error: unable to find token file.')
            exit(2)
    return tokenfile.readline()

def print_light_names(lightsJson):
    print('Your lights:')
    for i in range(len(lightsJson)):
        print(i, ': ', lightsJson[i].get(LIGHT_NAME), sep="")

def build_payload(args):
    payload = {}
    for i in args.keys():
        if i == KELVIN:
            color = 'kelvin:' + args.get(i)
            payload[COLOR] = color
        else:
            payload[i] = args.get(i)

    return payload