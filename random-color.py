#!/usr/bin/env python3

# taken from iterm2 python api docs:
#   https://www.iterm2.com/python-api/examples/random_color.html

import iterm2
import random
import colorsys
import os
from pprint import pprint, pformat

last_value_path="/Users/devgru/.iterm-last-hue"

def get_last_hue():
    default = 0.0
    if not os.path.isfile(last_value_path):
        set_last_hue(0.0)

    with open(last_value_path, "r") as ifh:

        try:
            hue_raw = ifh.readline()
        except FileNotFoundError as e:
            print("AAAAAUUUUUUGGGGGGHHHHHHH: File not found!: ", e)

        try:
            hue = float(hue_raw)
            return hue
        except ValueError as e:
            print("AAAAAUUUUUUGGGGGGHHHHHHH: Unable to read as float: ", e)

    return default

def set_last_hue(hue):

    try:
        hue = float(hue)
    except ValueError:
        print("Unable to read as float")
        return

    with open(last_value_path, "w") as ofh:
        ofh.write(str(hue))



alpha = int(255 * 0.80)
# init_c = (0, 0.8, 1.0)                  # rgb
# init_c_hls = colorsys.rgb_to_hls(       # hls
#     init_c[0],
#     init_c[1],
#     init_c[2],
# )

async def SetRandomColorInSession(connection, session, preset_name):
    # set random color
    ## randomly adjust hue and convert to rgb
    print("randomly adjust hue and convert to rgb")

    last_hue = get_last_hue()
    hue = last_hue

    while abs(last_hue - hue) < 0.1 or abs(last_hue - hue + 1.0) < 0.1 or abs(last_hue - hue - 1.0) < 0.1:
        print("    generating new hue...")
        hue = random.random()

    set_last_hue(hue)

    c = colorsys.hls_to_rgb(
        hue,
        0.2,
        0.5,
    )
    pprint(c)

    ## convert to 255 scale
    c = iterm2.color.Color(
        int(c[0] * 255),
        int(c[1] * 255),
        int(c[2] * 255),
        alpha
    )


    # get profile
    print("getting profile...")
    profile = await session.async_get_profile()
    if not profile:
        return

    print("setting backgorund color...")
    await profile.async_set_background_color(c)
    # profile.set_background_color(c)


# async def SetPresetInSession(connection, session, preset_name):

#     preset = await iterm2.ColorPreset.async_get(connection, preset_name)
#     if not preset:
#         return
#     profile = await session.async_get_profile()
#     if not profile:
#         return
#     await profile.async_set_color_preset(preset)

async def main(connection):

    app = await iterm2.async_get_app(connection)

    color_preset_names = await iterm2.ColorPreset.async_get_list(connection)


    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            session = app.get_session_by_id(session_id)
            if session:
                # await SetPresetInSession(connection, session, random.choice(color_preset_names))
                await SetRandomColorInSession(connection, session, random.choice(color_preset_names))
                

iterm2.run_forever(main)
