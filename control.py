#!/usr/bin/python

import requests
import ConfigParser
import sys
import os
import argparse
import json
from collections import OrderedDict
from ast import literal_eval
# import inspect # Debug

URI = 'https://software.imdea.org/intranet/'

conf_word = 'credentials'
conf_filename = '.credentials'
conf_template_filename = '.credentials.template'
conf_filepath = os.path.abspath(os.path.dirname(__file__)) + '/' + conf_filename

ROOM = 0

data = ['Climate Control Status', 'Climate control fan speed',
        'Climate control mode', 'Manual Door Light Setting',
        'Manual Window Light Setting', 'Sunblind Control',
        'Sunblind Setting', 'Temperature Setting', 'blind', 'climate_control',
        'climate_mode', 'door_is_closed', 'door_light', 'door_light_control',
        'door_open', 'fanspeed', 'lux_level', 'temp', 'temp_set',
        'window_is_closed', 'window_light', 'window_light_control']

states = OrderedDict([('temp', 'Current Temperature'),
                      ('temp_set', 'Target Temperature'),
                      ('climate_control', 'Climate Control State'),
                      ('climate_mode', 'Climate Control Mode'),
                      ('fanspeed', 'Climate Control Fan Speed'),
                      ('lux_level', 'Lux Level'),
                      ('door_light', 'Door Light Level'),
                      ('door_light_control', 'Door Light Mode'),
                      ('window_light', 'Window Light Level'),
                      ('window_light_control', 'Window Light Mode'),
                      ('blind', 'Roller Blinds Level')])

args_text = {'temp': 'temperature',
             'window_light': 'window light',
             'door_light': 'door light',
             'fanspeed': 'fan speed',
             'climate_mode': 'climate mode',
             'climate_control': 'climate control',
             'blind': 'roller blind'}

controls = {'temp': 'temp',
            'window': 'window_light',
            'door': 'door_light',
            'lights': '("window_light", "door_light")',
            'fspeed': 'fanspeed',
            'clmode': 'climate_mode',
            'clcontrol': 'climate_control',
            'blind': 'blind',
            'opdoor': 'door_open'}

defaults = {'door_light': 'OFF',
            'window_light': 'OFF',
            'blind': '10',
            'climate_mode': 'FAN_ONLY',
            'climate_control': 'OFF',
            'fanspeed': '100',
            'temp': '25'}

other_room_conf = {
    'winter_heat' :
            {'door_light': 'AUTO',
            'window_light': 'AUTO',
            'blind': '80',
            'climate_mode': 'HEAT',
            'climate_control': 'ON',
            'fanspeed': '100',
            'temp': '23'},
    'summer_cold' : {'door_light': 'AUTO',
            'window_light': 'AUTO',
            'blind': '80',
            'climate_mode': 'COLD',
            'climate_control': 'ON',
            'fanspeed': '100',
            'temp': '25'}
}

cc_values = ['ON', 'OFF']
cm_values = ['HEAT', 'COOL', 'FAN_ONLY']
fs_values = ['25', '50', '75', '100']
l_values = ['OFF', 'AUTO']


class bcolors:
    HEADER = '\033[94m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ProcessingConfig:
    '''
    Class to store IMDEA credentials
    '''
    def __init__(self, filepath=conf_filepath):
        self.filepath = filepath

        # Check if conf_filepath exists
        if not os.path.exists(filepath):
            print 'Filepath \"{}\" does not exist'\
                .format(os.path.abspath(filepath))
            file_format()
            sys.exit(1)

        # Parse config file
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(filepath))

        # IMDEA Credentials
        try:
            self.user = config.get(conf_word, 'user')
            self.passwd = config.get(conf_word, 'pass')
            self.room = config.getint(conf_word, 'room')

        except Exception:
            file_format()
            sys.exit(1)


def author():
    print "\t"+"-" * 55
    print "\t| {3}{0: <15}{5} | {4}{1: <15}{5} | {4}{2: >15}{5} |"\
        .format("Author", "Sergio Chica", "@scmanjarrez",
                bcolors.HEADER, bcolors.OK, bcolors.ENDC)
    print "\t| {3}{0: <15}{5} | {4}{1: <15}{5} | {4}{2: >15}{5} |"\
        .format("Acknowledgment", "Sergio Valverde", "@svg153",
                bcolors.HEADER, bcolors.OK, bcolors.ENDC)
    print "\t"+"-" * 55
    print "\t| {1}{0: ^51}{2} |"\
        .format("IMDEA Software Institute",
                bcolors.HEADER, bcolors.ENDC)
    print "\t"+"-" * 55
    print "\t| {1}{0: ^51}{2} |"\
        .format("2016-2017",
                bcolors.HEADER, bcolors.ENDC)
    print "\t"+"-" * 55


def file_format():
    print "File should be named \""+conf_filename+"\"",
    print "or indicate the path with the -cf argument."
    print ""
    print "Please copy the file \""+conf_template_filename+"\""
    print "to \""+conf_filename+"\" and put your IMDEA Software"
    print "user, password and room, inside the file."


def set_default(session, conf=defaults):
    find  = False
    if conf != 'defaults':
        for other_conf in other_room_conf:
            if other_conf == conf:
                find  = True
                print bcolors.HEADER\
                    + "\t[+] INFO: Setting room with"\
                    + " '" + conf + "' "\
                    + "setings:"\
                    + bcolors.ENDC
                for confI in other_room_conf[conf]:
                    set_control(session, confI, other_room_conf[conf][confI])
        if not find:
            print bcolors.ERROR\
                + "\t[-] The configuration room"\
                + " '" + conf + "' "\
                + "does not exist."\
                + bcolors.ENDC
    else:
        for dflt in defaults:
            set_control(session, dflt, defaults[dflt])


def set_control(session, control, value):
    if check_control_value(control, value):
        return

    if control == 'door_open':
            print bcolors.HEADER\
                + "\t[+] INFO: Opening door..."\
                + bcolors.ENDC,
    else:
        print bcolors.HEADER\
            + "\t[+] INFO: Setting "+args_text[control]+" to "+value+"..."\
            + bcolors.ENDC,
    resp = session.get(make_set_url(control, value))

    try:
        if json.loads(resp.text)['ok'] is not True:
            print bcolors.ERROR\
                + "ERROR"
            print "\t\t[-] Control "+states[control]\
                + " could not be set to "+value+"."\
                + bcolors.ENDC
        else:
            print bcolors.OK\
                + "OK"\
                + bcolors.ENDC
    except:
        print bcolors.ERROR\
            + "ERROR"
        print "\t\t[-] Problems with the server, retry later."\
            + bcolors.ENDC


def check_control_value(control, value):
    if control == 'fanspeed':
        if value not in fs_values:
            print bcolors.ERROR\
                + "\t[-] ERROR: Fan speed can only be set to "\
                + "/".join(fs_values)+"."\
                + bcolors.ENDC
            return 1

    elif control in ('door_light', 'window_light'):
        if value.upper() not in l_values:
            try:
                if (int(value) > 100 or int(value) < 0):
                    print bcolors.ERROR\
                        + "\t[-] ERROR: Light can only be set to "\
                        + "/".join(l_values)+" or 0-100."\
                        + bcolors.ENDC
                    return 1
            except:
                print bcolors.ERROR\
                    + "\t[-] ERROR: Light can only be set to "\
                    + "/".join(l_values)+" or 0-100."\
                    + bcolors.ENDC
                return 1

    elif control == 'climate_mode':
        if value.upper() not in cm_values:
            print bcolors.ERROR\
                + "\t[-] ERROR: Climate mode can only be set to "\
                + "/".join(cm_values)+"."\
                + bcolors.ENDC
            return 1

    elif control == 'climate_control':
        if value.upper() not in cc_values:
            print bcolors.ERROR\
                + "\t[-] ERROR: Climate control can only be set to "\
                + "/".join(cc_values)+"."\
                + bcolors.ENDC
            return 1

    elif control == 'temp':
        try:
            if float(value) > 28 or float(value) < 16:
                print bcolors.ERROR\
                    + "\t[-] ERROR: Temperature can only be set to 16.0-28.0."\
                    + bcolors.ENDC
                return 1
        except:
            print bcolors.ERROR\
                + "\t[-] ERROR: Temperature can only be set to 16.0-28.0."\
                + bcolors.ENDC
            return 1

    return 0


def make_get_url():
    return URI+"control/get/"+str(ROOM)


def make_set_url(control, value):
    return URI+"control/set/"+str(ROOM)+"/"+control+"/"+value


def get_current_state(session):
    req = session.get(make_get_url())
    jsn = json.loads(req.text)['data']

    print "\t"+"-" * (2+30+3+10+2)
    print "\t| {: ^30} | {: ^10} |".format("Control", "Value")
    print "\t"+"-" * (2+30+3+10+2)
    for dt in states:
        print "\t| {0}{1: <30}{2} | {3}{4: >10}{2} |"\
            .format(bcolors.HEADER, states[dt],
                    bcolors.ENDC, bcolors.OK, jsn[dt])

    print "\t"+"-" * (2+30+3+10+2)


def login(config, args):
    session = requests.session()
    req = session.post(URI, data={'action': 'login',
                                  'user': config.user,
                                  'pass': config.passwd})

    if req.text.find('Welcome') == -1:
        print bcolors.ERROR\
            + "\t[-] ERROR: Login could not be completed, "\
            + "check your "+conf_word+"."\
            + bcolors.ENDC
        sys.exit(1)

    global ROOM
    if args.room:
        ROOM = args.room
    else:
        ROOM = config.room

    return session


def main(argparser, args):
    if args.conf:
        config = ProcessingConfig(args.conf)
    else:
        config = ProcessingConfig()

    session = login(config, args)

    if args.state:
        get_current_state(session)
    elif args.default:
        actions = list_used_options(argparser, args)
        for act in actions:
            set_default(session, act[1])
    else:
        actions = list_used_options(argparser, args)
        for act in actions:
            if act[0] == 'lights':
                lights = literal_eval(controls[act[0]])
                set_control(session, lights[0], act[1])
                set_control(session, lights[1], act[1])
            elif act[0] == 'opdoor':
                set_control(session, controls[act[0]], '0')
            else:
                set_control(session, controls[act[0]], act[1])


def list_used_options(parser, args):
    actions = [action for action in parser._optionals._actions
               if getattr(args, action.dest, action.default)
               is not action.default]
    # _StoreAction(option_strings=['-t', '--temp'],
    # dest='temp', nargs=None, const=None, default=None,
    # type=None, choices=None, help='Set the temperature.', metavar=None)
    values = vars(args)
    act = [act._get_kwargs()[0][1][1].split('--')[1] for act in actions]
    return [(action, values[action]) for action in act]


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(prog='control',
                                        description='Allow control IMDEA'
                                        + ' building automation parameters.')

    argparser.add_argument('-cf', '--conf',
                           help='If set, uses specific configuration file.')

    argparser.add_argument('-ff', '--file_format',
                           help='Show '+conf_filename+' file format.',
                           action='store_true')

    argparser.add_argument('-at', '--author',
                           help='Show author information.',
                           action='store_true')

    argparser.add_argument('-r', '--room',
                           help='If set, modifies specific room.')

    group = argparser.add_argument_group('mandatory arguments')

    group.add_argument('-st', '--state',
                       help='Get current state.',
                       action='store_true')

    group.add_argument('-def', '--default',
                       # nargs='?', const='defaults'
                       help='Set the room with a preconfigure setings.')

    group.add_argument('-t', '--temp',
                       help='Set the temperature.')

    group.add_argument('-w', '--window',
                       help='Set the window light.')

    group.add_argument('-d', '--door',
                       help='Set the door light.')

    group.add_argument('-b', '--blind',
                       help='Set the roller blinds.')

    group.add_argument('-l', '--lights',
                       help='Set all the lights.')

    group.add_argument('-f', '--fspeed',
                       help='Set the fan speed.')

    group.add_argument('-m', '--clmode',
                       help='Set the climate mode.')

    group.add_argument('-c', '--clcontrol',
                       help='Set the climate control.')

    group.add_argument('-op', '--opdoor',
                       help='Open the door.',
                       action='store_true')

    args = argparser.parse_args()

    # Method debug
    # for x in inspect.getmembers(action, predicate=inspect.ismethod):
    #     print x

    if not any(vars(args).values()):
        argparser.error("No argument provided.")

    if args.file_format:
        file_format()
        sys.exit()

    if args.author:
        author()
        sys.exit()

    print bcolors.HEADER\
        + "[+] Script started"\
        + bcolors.ENDC
    main(argparser, args)
