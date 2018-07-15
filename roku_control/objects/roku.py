import configparser
import os
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('/usr/local/bin/homeapi/roku_control/configs/roku.ini')


class Roku:
    def __init__(self, location):
        self.location = location
        # self.ip = config['device']['deprecated_devices'][self.location]
        self.ip = config['device'][self.location]
        self.url = "http://{}:{}/".format(self.ip, config['device']['port'])
        # self.sn = None
        # self.deviceid = None
        # self.devicename = None
        # self.modelnum = None
        # self.model = None
        # self.wifimac = None
        # self.ethernetmac = None
        # self.network = None
        # self.version = None
        # self.build = None
        # self.power = None
        # self.suspend = None
        # self.findremote = None
        # self.search = None
        # self.voicesearch = None
        # self.notifications = None
        # self.privatelistening = None
        # self.headphones = None
        # self._get_details()

    def _find_app_id(self, app):
        """Find the ID of an app"""
        soup = BeautifulSoup(os.popen("curl {}/query/apps".format(self.url)), "lxml-xml")
        app_id = soup.find("app", text="{}".format(app))['id']
        return app_id

    def _get_details(self):
        """Complete the instantiation"""
        soup = BeautifulSoup(os.popen("curl {}/query/device-info".format(self.url)), "lxml-xml")
        self.sn = soup.find('serialNumber').contents
        self.deviceid = soup.find('device-id').contents
        self.devicename = soup.find('user-device-name').contents
        self.modelnum = soup.find('model-number').contents
        self.model = soup.find('model-name').contents
        self.wifimac = soup.find('wifi-mac').contents
        if soup.find('supports-ethernet').contents:
            self.ethernetmac = soup.find('ethernet-mac').contents
        self.network = soup.find('network-type').contents
        self.version = soup.find('software-version').contents
        self.build = soup.find('software-build').contents
        self.power = soup.find('power-mode').contents
        self.suspend = soup.find('supports-suspend').contents
        self.findremote = soup.find('supports-find-remote').contents
        self.search = soup.find('search-enabled').contents
        self.voicesearch = soup.find('voice-search-enabled').contents
        self.notifications = soup.find('notifications-enabled').contents
        self.privatelistening = soup.find('supports-private-listening').contents
        self.headphones = soup.find('headphones-connected').contents

    def _signin_plex(self, profile):
        """Sign into Plex using the profile"""
        user = list(filter(lambda user: user['name'] == profile, config['plex']['profile']))[0]
        sequence = ['Select',
                    config['plex']['num_buttons'][user['code'][0]],
                    config['plex']['num_buttons'][user['code'][1]],
                    config['plex']['num_buttons'][user['code'][2]],
                    config['plex']['num_buttons'][user['code'][3]],
                    'Select']
        # Add the correct number of Lit_R button presses to the sequence
        for i in range(0, config['plex']['profile']['location']):
            sequence.insert(0, 'Lit_R')
        for button in sequence:
            self.press_button({button})

    def find_remote(self):
        """Activate the Find Remote Functionality"""
        self.press_button('FindRemote')

    def list_apps(self):
        """List all installed apps on the Roku"""
        os.popen("curl -d '' {}/query/apps".format(self.url))

    def press_button(self, button):
        """Press a button on the Roku"""
        os.popen("curl -d '' {}/keypress/{}".format(self.url, button))

    def run_app(self, app, profile=None):
        """Open an app on the Roku"""
        app_id = self._find_app_id(app)
        os.popen("curl -d '' {}/launch/{}".format(self.url, app_id))
        if app == 'plexpass' and profile != None:
            self._signin_plex(profile)
        else:
            print('Plex user was not defined...')

    def set_sleep_timer(self, time):
        """Power Off the Roku in <time> minutes"""
        time = time * 60
        os.popen("sleep {}; curl -d '' {}/keypress/PowerOff".format(time, self.url))


def main():
    pass

if __name__ == '__main__':
    main()
