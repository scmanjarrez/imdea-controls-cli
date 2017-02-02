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

conf_filepath = os.path.abspath(os.path.dirname(__file__)) + '/.credentials'

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

controls = {'temp': 'temp',
            'window': 'window_light',
            'door': 'door_light',
            'lights': '("window_light", "door_light")',
            'fspeed': 'fanspeed',
            'clmode': 'climate_mode',
            'clcontrol': 'climate_control',
            'opdoor': 'door_open'}

defaults = {'door_light': 'OFF',
            'window_light': 'OFF',
            'blind': '10',
            'climate_mode': 'FAN_ONLY',
            'climate_control': 'OFF',
            'fanspeed': '100',
            'temp': '25'}

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
            self.user = config.get('credentials', 'user')
            self.passwd = config.get('credentials', 'pass')
            self.room = config.getint('credentials', 'room')

        except Exception:
            file_format()
            sys.exit(1)


def author():
    print "Author: Sergio Chica, @scmanjarrez"
    print "Acknowledgment: Sergio Valverde, @svg153"
    print "IMDEA Software Institute"
    print "2016-2017"


def file_format():
    print "File should be named \".credentials\"",
    print "or indicate the path with the -cf argument"
    print "and must have the following format:"
    print ""
    print "[credentials]"
    print "user = Your_IMDEA_User"
    print "pass = Your_IMDEA_Pass"
    print "room = Room_to_modify"


def set_default(session):
    for dflt in defaults:
        set_control(session, dflt, defaults[dflt])


def set_control(session, control, value):
    if check_control_value(control, value):
        return

    print bcolors.HEADER\
        + "\t[+] INFO: Setting "+control+" to "+value+"..."\
        + bcolors.ENDC,
    resp = session.get(make_set_url(control, value))

    try:
        if json.loads(resp.text)['ok'] is not True:
            print bcolors.ERROR\
                + "ERROR"
            print "\t\t[-] Control "+control+" could not be set to "+value+"."\
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
        print "\t| {}{: <30}{} | {}{: >10}{} |"\
            .format(bcolors.HEADER, states[dt], bcolors.ENDC,
                    bcolors.OK, jsn[dt], bcolors.ENDC)

    print "\t"+"-" * (2+30+3+10+2)


def login(config):
    session = requests.session()
    req = session.post(URI, data={'action': 'login',
                                  'user': config.user,
                                  'pass': config.passwd})

    if req.text.find('Welcome') == -1:
        print bcolors.ERROR\
            + "\t[-] ERROR: Login could not be completed, "\
            + "check your credentials."\
            + bcolors.ENDC
        sys.exit(1)

    global ROOM
    ROOM = config.room

    return session


def main(argparser, args):
    if args.conf:
        config = ProcessingConfig(args.conf)
    else:
        config = ProcessingConfig()

    session = login(config)

    if args.state:
        get_current_state(session)
    elif args.default:
        set_default(session)
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
                           help='If set, specify configuration file path.')

    argparser.add_argument('-ff', '--file_format',
                           help='Show credentials file format.',
                           action='store_true')

    argparser.add_argument('-at', '--author',
                           help='Show author information.',
                           action='store_true')

    group = argparser.add_argument_group('mandatory arguments')

    group.add_argument('-st', '--state',
                       help='Get current state.',
                       action='store_true')

    group.add_argument('-def', '--default',
                       help='Set the default values.',
                       action='store_true')

    group.add_argument('-t', '--temp',
                       help='Set the temperature.')

    group.add_argument('-w', '--window',
                       help='Set the window light.')

    group.add_argument('-d', '--door',
                       help='Set the door light.')

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
        + "Starting script..."\
        + bcolors.ENDC
    main(argparser, args)
