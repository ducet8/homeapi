#! /usr/local/bin/python3
# Py Vers : 3.6.5
#
# Title   : roku_control.py
# Purpose : This script will control a Roku
# Note    : https://sdkdocs.roku.com/display/sdkdoc/External+Control+API
# History : 4/15/18 RLT - Initial Creation
################################################################################
import click
from objects import roku


@click.command()
@click.argument('location')
@click.option('--press', '-p', help='Press a button')
@click.option('--run', '-r', help='Run an app')
@click.option('--sleep', '-s', default=30, help='Set a sleep timer in minutes\nDefault=30 minutes')
@click.option('--find_remote', is_flag=True, help='Activate the find remote feature')
@click.option('--plexuser', type=click.Choice(['<PROFILE_1_NAME>',
    '<PROFILE_2_NAME>']), help='The user profile to open in Plex')
def main(location, press, run, sleep, find_remote, plexuser):
    roku_obj = roku.Roku(location)
    if press:
        roku_obj.press_button(press)
    elif run:
        if run == 'plexpass' and plexuser != None:
            roku_obj.run_app(run, plexuser)
        else:
            roku_obj.run_app(run)
    elif sleep:
        roku_obj.set_sleep_timer(int(sleep))
    elif find_remote:
        # roku_obj.find_remote()
        roku_obj.press_button('FindRemote')
    else:
        print('You did not specify an action.')


if __name__ == '__main__':
    main()
