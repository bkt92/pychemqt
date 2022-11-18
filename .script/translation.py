#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Script to update i18n/pychemqt.pro with new files

# Next the ts files must be generated with
# pylupdate5 pychemqt.pro

# The translation can be done with linguist
# When translation done make the translation release
# lrelease pychemqt_es.ts


import glob


# Define the language translation to generate
LANGUAGES = ["es"]


with open("/home/jjgomera/Programacion/pychemqt/i18n/pychemqt.pro", "w") as file:
    print("# File autogenerated by .script/translation.py", file=file)
    print("# Do not edit, run that script", file=file)
    print("", file=file)

    lst = glob.iglob("/home/jjgomera/Programacion/pychemqt/**/*.py", recursive=True)
    for path in lst:
        shortpath = path.replace("/home/jjgomera/Programacion/pychemqt", "..")
        print("SOURCES += ", shortpath, file=file)
    print("", file=file)

    # Add translation
    for lng in LANGUAGES:
        print("TRANSLATIONS += pychemqt_%s.ts" % lng, file=file)
