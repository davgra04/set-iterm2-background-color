#!/usr/bin/env python3

# taken from iterm2 python api docs:
#   https://www.iterm2.com/python-api/examples/random_color.html

import iterm2
import random
import colorsys
import os
from pprint import pprint, pformat

################################################################################
# configuration
################################################################################

homedir = os.path.expanduser("~")
last_value_path=f"{homedir}/.iterm-last-hue"     # stores the last used hue value
min_h_diff = 0.3        # limit to hues that are a minimum distance away from the last value

# alpha not currently doing anything! Adjust background transparency in preferences
alpha = 0.10        # window background opacity     (0 - 1.0)  
lightness = 0.20    # window background lightness   (0 - 1.0)
saturation = 0.80   # window background saturation  (0 - 1.0)

################################################################################
# functions
################################################################################

def get_last_hue():
    """reads the last hue value from disk"""
    default = 0.0
    if not os.path.isfile(last_value_path):
        set_last_hue(0.0)

    with open(last_value_path, "r") as ifh:

        try:
            hue_raw = ifh.readline()
        except FileNotFoundError as e:
            print("AAAAAUUUUUUGGGGGGHHHHHHH: File not found!: ", e)
            exit()

        try:
            hue = float(hue_raw)
            return hue
        except ValueError as e:
            print("AAAAAUUUUUUGGGGGGHHHHHHH: Unable to read as float: ", e)
            exit()

    return default

def set_last_hue(hue):
    """saves new last hue value to disk"""
    try:
        hue = float(hue)
    except ValueError:
        print("Unable to read as float")
        return

    with open(last_value_path, "w") as ofh:
        ofh.write(str(hue))

async def SetRandomColorInSession(connection, session, preset_name):
    """sets background of current iTerm2 session to a random color"""

    ## randomly adjust hue and convert to rgb
    print("randomly adjust hue and convert to rgb")
    last_hue = get_last_hue()
    hue = last_hue

    while abs(last_hue - hue) < min_h_diff or abs(last_hue - hue + 1.0) < min_h_diff or abs(last_hue - hue - 1.0) < min_h_diff:
        print("    generating new hue...")
        hue = random.random()

    set_last_hue(hue)

    c = colorsys.hls_to_rgb(
        hue,
        lightness,
        saturation,
    )
    pprint(c)

    ## convert to 255 scale
    c = iterm2.color.Color(
        int(c[0] * 255),
        int(c[1] * 255),
        int(c[2] * 255),
        int(alpha * 255)
    )

    # get profile
    print("getting profile...")
    profile = await session.async_get_profile()
    if not profile:
        print("couldn't get profile!")
        return

    print("setting background color...")
    await profile.async_set_background_color(c)

################################################################################
# main function
################################################################################

async def main(connection):
    app = await iterm2.async_get_app(connection)
    color_preset_names = await iterm2.ColorPreset.async_get_list(connection)

    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            session = app.get_session_by_id(session_id)
            if session:
                await SetRandomColorInSession(connection, session, random.choice(color_preset_names))

iterm2.run_forever(main)
