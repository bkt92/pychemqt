#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2017, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


###############################################################################
# Library function for plugin
#   - getClassFluid: Return the thermo class to calculate
#   - getMethod: Return the thermo method name to use
#   - calcPoint: Calculate point state and check state in P-T range of eq
#   - get_propiedades: Get the properties to show in tables
#   - _getData: Get values of properties in fluid
###############################################################################


from configparser import ConfigParser

from lib import mEoS, coolProp, refProp, config, unidades
from lib.thermo import ThermoAdvanced


N_PROP = len(ThermoAdvanced.properties())
KEYS = ThermoAdvanced.propertiesKey()
UNITS = ThermoAdvanced.propertiesUnit()


def getClassFluid(conf):
    """Return the thermo class to calculate
    Really return the base instance to add kwargs to calculate"""
    pref = ConfigParser()
    pref.read(config.conf_dir + "pychemqtrc")

    if pref.getboolean("MEOS", 'coolprop') and \
            pref.getboolean("MEOS", 'refprop'):
        # RefProp case, the base instance with the ids kwargs to define the
        # defined compount
        id = mEoS.__all__[conf.getint("MEoS", "fluid")].id
        fluid = refProp.RefProp(ids=[id])

    elif pref.getboolean("MEOS", 'coolprop'):
        # CoolProp case, the base instance with the ids kwargs to define the
        # defined compount
        id = mEoS.__all__[conf.getint("MEoS", "fluid")].id
        fluid = coolProp.CoolProp(ids=[id])

    else:
        # MEOS case, the instance of specified mEoS subclass
        fluid = mEoS.__all__[conf.getint("MEoS", "fluid")]()

    return fluid


def getMethod():
    """Return the thermo method name to use"""
    pref = ConfigParser()
    pref.read(config.conf_dir + "pychemqtrc")

    if pref.getboolean("MEOS", 'coolprop') and \
            pref.getboolean("MEOS", 'refprop'):
        txt = "REFPROP"
    elif pref.getboolean("MEOS", 'coolprop'):
        txt = "COOLPROP"
    else:
        txt = "MEOS"
    return txt


def calcPoint(fluid, config, **kwargs):
    """Procedure to calculate point state and check state in P-T range of eq"""
    method = getMethod()
    if method == "MEOS":
        if isinstance(config, dict):
            option = config
        else:
            option = {}
            option["eq"] = config.getint("MEoS", "eq")
            option["visco"] = config.getint("MEoS", "visco")
            option["thermal"] = config.getint("MEoS", "thermal")
        kwargs.update(option)
        Tmin = fluid.eq[option["eq"]]["Tmin"]
        Tmax = fluid.eq[option["eq"]]["Tmax"]
        Pmin = fluid(T=fluid.eq[option["eq"]]["Tmin"], x=0).P
        Pmax = fluid.eq[option["eq"]]["Pmax"]*1000
    elif method == "COOLPROP":
        Tmin = fluid.eq["Tmin"]
        Tmax = fluid.eq["Tmax"]
        Pmin = fluid.eq["Pmin"]
        Pmax = fluid.eq["Pmax"]
    elif method == "REFPROP":
        pass

    if "T" in kwargs:
        if kwargs["T"] < Tmin or kwargs["T"] > Tmax:
            return None
    if "P" in kwargs:
        if kwargs["P"] < Pmin-1 or kwargs["P"] > Pmax+1:
            return None
    fluido = fluid._new(**kwargs)

    if fluido.status not in [1, 3]:
        return None

    if method == "MEOS":
        if fluido._melting and fluido._melting["Tmin"] <= fluido.T\
                <= fluido._melting["Tmax"]:
            Pmel = fluido._Melting_Pressure(fluido.T)
            Pmax = min(Pmax, Pmel)

    if fluido.P < Pmin-1 or fluido.P > Pmax+1 or fluido.T < Tmin\
            or fluido.T > Tmax:
        return None
    return fluido


def get_propiedades(config):
    """Procedure to get the properties to show in tables
    Input:
        config: configparser instance with mainwindow preferences
    Output:
        array with properties, key and units
    """
    booleanos = config.get("MEoS", "properties")
    order = config.get("MEoS", "propertiesOrder")
    if isinstance(booleanos, str):
        booleanos = eval(booleanos)
    if isinstance(order, str):
        order = eval(order)

    propiedades = []
    keys = []
    units = []
    for indice, bool in zip(order, booleanos):
        if bool:
            name, key, unit = ThermoAdvanced.properties()[indice]
            propiedades.append(name)
            keys.append(key)
            units.append(unit)
    return propiedades, keys, units


def _getData(fluid, keys, phase=True, unit=None, table=True):
    """Procedure to get values of properties in fluid
    Input:
        fluid: fluid instance to get values
        keys: array with desired parameter to get
        phase: boolean to get the properties values for both phases
        unit: unidades subclass
        table: boolean if the values are for a table, the none values are repr
            as text msg
    """
    fila = []
    for i, key in enumerate(keys):
        if not key:
            continue
        p = fluid.__getattribute__(key)
        if isinstance(p, str):
            txt = p
        else:
            if unit and unit[i]:
                txt = p.__getattribute__(unit[i])
            else:
                txt = p.config()
        fila.append(txt)

        # Add two phases properties is requested
        if phase and key in ThermoAdvanced.propertiesPhase():
            # Liquid
            p = fluid.Liquido.__getattribute__(key)
            if isinstance(p, str):
                txt = p
            elif isinstance(p, unidades.unidad):
                if unit and unit[i]:
                    txt = p.__getattribute__(unit[i])
                else:
                    txt = p.config()
            else:
                txt = p
            fila.append(txt)
            # Gas
            p = fluid.Gas.__getattribute__(key)
            if isinstance(p, str):
                txt = p
            elif isinstance(p, unidades.unidad):
                if unit and unit[i]:
                    txt = p.__getattribute__(unit[i])
                else:
                    txt = p.config()
            else:
                txt = p
            fila.append(txt)
    return fila
