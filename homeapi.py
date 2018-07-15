#!/usr/local/bin/python3
import configparser
import os
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

application = Flask(__name__)
api = Api(application)

parser = reqparse.RequestParser()
parser.add_argument('button')
parser.add_argument('minutes')
parser.add_argument('app')
parser.add_argument('plexuser')


def abort_if_roku_doesnt_exist(roku_name):
    if roku_name not in config['device']['devices']:
        abort(404, message="Roku {} doesn't exist".format(roku_name))

class roku(Resource):
    config = configparser.ConfigParser()
    config.read('./roku_control/configs/roku.ini')

    def get(self, roku_name):
        abort_if_roku_doesnt_exist(roku_name)
        for device in range(0, len(config['device']['devices'].keys())):
            return list(config['device']['devices'].keys())[device]

    def post(self, roku_name, action):
        args = parser.parse_args()
        if action == 'press':
            os.popen('python3 ./roku_control/roku_control.py --press {} {}'.format(args["button"], roku_name))
            # print('python3 ./roku_control/roku_control.py --press {} {}'.format(args["button"], roku_name))
            return '', 204
        if action == 'sleep':
            os.popen('python3 ./roku_control/roku_control.py --sleep {} {}'.format(args["minutes"], roku_name))
            # print('python3 ./roku_control/roku_control.py --sleep {} {}'.format(args["minutes"], roku_name))
            return '', 204
        if action == 'run':
            if args['app'] == 'plexpass':
                if args['plexuser']:
                    os.popen('python3 ./roku_control/roku_control.py --run {} --plexuser {} {}'.format(args["app"], args["plexuser"], roku_name))
                    # print('python3 ./roku_control/roku_control.py --run {} --plexuser {} {}'.format(args["app"], args["plexuser"], roku_name))
                else:
                    os.popen('python3 ./roku_control/roku_control.py --run {} {}'.format(args["app"], roku_name))
                    # print('python3 ./roku_control/roku_control.py --run {} {}'.format(args["app"], roku_name))
                return '', 204
            else:
                os.popen('python3 ./roku_control/roku_control.py --run {} {}'.format(args["app"], roku_name))
                # print('python3 ./roku_control/roku_control.py --run {} {}'.format(args["app"], roku_name))
                return '', 204
        if action == 'find_remote':
            os.popen('python3 ./roku_control/roku_control.py --find_remote {}'.format(roku_name))
            # print('python3 ./roku_control/roku_control.py --find_remote {}'.format(roku_name))
            return '', 204


# API Resource Routing
api.add_resource(roku, '/roku/<roku_name>/<action>')

if __name__ == '__main__':
    application.run()
