#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2023, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""


###############################################################################
# Module with common thermal utilities:
#   - Thermo: Class with common functionality for special thermo model
#   - ThermoAdvanced: Thermo subclass with additional properties for advanced
#       meos model, coolprop, meos
#   - ThermoWater: Thermo subclass with water specific properties, for iapws as
#       iapws and freesteam
#   - ThermoRefProp: Thermo subclass with specific properties availables in
#       refprop
###############################################################################


from tools.qt import tr
from iapws._utils import getphase
from lib import unidades


class Thermo(object):
    """Class with common functionality for special thermo model, children class
    are iapws, coolprop, refprop"""

    _bool = False
    status = 0
    msg = "Unknown variables"
    kwargs = {}

    h = 0
    s = 0
    u = 0
    a = 0
    g = 0

    def __init__(self, **kwargs):
        self.kwargs = self.__class__.kwargs.copy()
        self.__call__(**kwargs)

    def _new(self, **kw):
        """Create a new instance"""
        # In refprop and coolprop classes the compound definition is fixed
        # so add to new instance initialization kwargs
        if "ids" in self.kwargs:
            kw["ids"] = self.kwargs["ids"]
        return self.__class__(**kw)

    def __call__(self, **kwargs):
        self.cleanOldValues(**kwargs)

        if self.calculable:
            self.status = 1
            self.msg = "Solved"
            self.calculo()
            self.cleanOldKwargs()

    def cleanOldValues(self, **kwargs):
        """Convert alternative input parameters"""
        pass

    def cleanOldKwargs(self, **kwargs):
        """Convert alternative input parameters"""
        pass

    def calculable(self):
        pass

    def calculo(self):
        pass

    def _cp0(self, cp0):
        "Set ideal properties to state"""
        self.v0 = unidades.SpecificVolume(cp0["v"])
        self.rho0 = unidades.Density(1./cp0["v"])
        self.h0 = unidades.Enthalpy(cp0["h"])
        self.u0 = unidades.Enthalpy(self.h0-self.P*self.v0)
        self.s0 = unidades.SpecificHeat(cp0["s"])
        self.a0 = unidades.Enthalpy(self.u0-self.T*self.s0)
        self.g0 = unidades.Enthalpy(self.h0-self.T*self.s0)

        self.cp0 = unidades.SpecificHeat(cp0["cp"])
        self.cv0 = unidades.SpecificHeat(cp0["cv"])
        self.cp0_cv = unidades.Dimensionless(self.cp0/self.cv0)
        self.w0 = unidades.Speed(cp0["w"])
        self.gamma0 = self.cp0_cv

        self.rhoM0 = unidades.MolarDensity(self.rho0/self.M)
        self.hM0 = unidades.MolarEnthalpy(self.h0*self.M)
        self.uM0 = unidades.MolarEnthalpy(self.u0*self.M)
        self.sM0 = unidades.MolarSpecificHeat(self.s0*self.M)
        self.aM0 = unidades.MolarEnthalpy(self.a0*self.M)
        self.gM0 = unidades.MolarEnthalpy(self.g0*self.M)
        self.cpM0 = unidades.MolarSpecificHeat(self.cp0*self.M)
        self.cvM0 = unidades.MolarSpecificHeat(self.cv0*self.M)

    def derivative(self, z, x, y, fase):
        """Calculate generic partial derivative: (δz/δx)y
        where x, y, z can be: P, T, v, u, h, s, g, a"""
        dT = {"P": 0,
              "T": 1,
              "v": fase.v*fase.alfav,
              "u": fase.cp-self.P*fase.v*fase.alfav,
              "h": fase.cp,
              "s": fase.cp/self.T,
              "g": -fase.s,
              "a": -self.P*fase.v*fase.alfav-fase.s}
        dP = {"P": 1,
              "T": 0,
              "v": -fase.v*fase.kappa,
              "u": fase.v*(self.P*fase.kappa-self.T*fase.alfav),
              "h": fase.v*(1-self.T*fase.alfav),
              "s": -fase.v*fase.alfav,
              "g": fase.v,
              "a": self.P*fase.v*fase.kappa}
        return (dP[z]*dT[y]-dT[z]*dP[y])/(dP[x]*dT[y]-dT[x]*dP[y])

    def getphase(self, **kwargs):
        """Return fluid phase
        kwarg:
            phase: direct msg
            Tc, Pc, T, P, x, region: to calculate by iapws"""
        data = {
            "Supercritical fluid": tr(
                "pychemqt", "Supercritical fluid"),
            "Gas": tr("pychemqt", "Gas"),
            "Compressible liquid": tr(
                "pychemqt", "Compressible liquid"),
            "Critical point": tr(
                "pychemqt", "Critical point"),
            "Saturated vapor": tr(
                "pychemqt", "Saturated vapor"),
            "Saturated liquid": tr(
                "pychemqt", "Saturated liquid"),
            "Two phases": tr("pychemqt", "Two phases"),
            "Vapour": tr("pychemqt", "Vapour"),
            "Liquid": tr("pychemqt", "Liquid"),
            "Unknown": tr("pychemqt", "Unknown")}

        if "phase" in kwargs:
            phase = kwargs["phase"]
        else:
            phase = getphase(**kwargs)
        return data[phase]

    @classmethod
    def properties(cls):
        l = [
            (tr("pychemqt", "Temperature"), "T",
             unidades.Temperature),
            (tr("pychemqt", "Reduced temperature"), "Tr",
             unidades.Dimensionless),
            (tr("pychemqt", "Pressure"), "P",
             unidades.Pressure),
            (tr("pychemqt", "Reduced Pressure"), "Pr",
             unidades.Dimensionless),
            (tr("pychemqt", "Quality"), "x",
             unidades.Dimensionless),
            (tr("pychemqt", "Density"), "rho",
             unidades.Density),
            (tr("pychemqt", "Molar Density"), "rhoM",
             unidades.MolarDensity),
            (tr("pychemqt", "Volume"), "v",
             unidades.SpecificVolume),
            (tr("pychemqt", "Enthalpy"), "h",
             unidades.Enthalpy),
            (tr("pychemqt", "Molar Enthalpy"), "hM",
             unidades.MolarEnthalpy),
            (tr("pychemqt", "Entropy"), "s",
             unidades.SpecificHeat),
            (tr("pychemqt", "Molar Entropy"), "sM",
             unidades.MolarSpecificHeat),
            (tr("pychemqt", "Internal Energy"), "u",
             unidades.Enthalpy),
            (tr("pychemqt", "Molar Internal Energy"), "uM",
             unidades.MolarEnthalpy),
            (tr("pychemqt", "Helmholtz Free Energy"), "a",
             unidades.Enthalpy),
            (tr("pychemqt", "Molar Helmholtz Free Energy"),
             "aM", unidades.MolarEnthalpy),
            (tr("pychemqt", "Gibbs Free Energy"), "g",
             unidades.Enthalpy),
            (tr("pychemqt", "Molar Gibbs Free Energy"),
             "gM", unidades.MolarEnthalpy),
            (tr(
                "pychemqt", "Specific isochoric heat capacity"), "cv",
                unidades.SpecificHeat),
            (tr(
                "pychemqt", "Molar Specific isochoric heat capacity"), "cvM",
                unidades.MolarSpecificHeat),
            (tr
             ("pychemqt", "Specific isobaric heat capacity"), "cp",
             unidades.SpecificHeat),
            (tr(
                "pychemqt", "Molar Specific isobaric heat capacity"), "cpM",
                unidades.MolarSpecificHeat),
            (tr("pychemqt", "Heat capacities ratio"),
             "cp_cv", unidades.Dimensionless),
            (tr("pychemqt", "Speed sound"), "w",
             unidades.Speed),
            (tr("pychemqt", "Compresibility"), "Z",
             unidades.Dimensionless),
            (tr("pychemqt", "Fugacity coefficient"), "fi",
             unidades.Dimensionless),
            (tr("pychemqt", "Fugacity"), "f",
             unidades.Pressure),
            (tr("pychemqt", "Isoentropic exponent"),
             "gamma", unidades.Dimensionless),
            (tr("pychemqt", "Volume Expansivity"), "alfav",
             unidades.InvTemperature),  # 1/V dV/dt = -1/D dD/dt
            (tr("pychemqt", "Isothermal compresibility"),
             "kappa", unidades.InvPressure),  # -1/V (dV/dP)T = 1/D (dD/dP)T
            (tr("pychemqt", "Adiabatic compresibility"),
             "kappas", unidades.InvPressure),  # -1/V (dV/dP)s = 1/D (dD/dP)s
            (tr(
                "pychemqt", "Relative pressure coefficient"), "alfap",
                unidades.InvTemperature),  # 1/P (dP/dT)v
            (tr(
                "pychemqt", "Isothermal stress coefficient"), "betap",
                unidades.Density),  # -1/P (dP/dv)T = 1/P (dP/dD)T
            (tr("pychemqt", "Joule-Thomson coefficient"),
             "joule", unidades.TemperaturePressure),
            (tr(
                "pychemqt", "Isothermal throttling coefficient"), "deltat",
                unidades.EnthalpyPressure),
            (tr("pychemqt", "Vaporization heat"), "Hvap",
             unidades.Enthalpy),
            (tr("pychemqt", "Vaporization entropy"),
             "Svap", unidades.SpecificHeat),
            (tr("pychemqt", "Viscosity"), "mu",
             unidades.Viscosity),
            (tr("pychemqt", "Thermal conductivity"), "k",
             unidades.ThermalConductivity),
            (tr("pychemqt", "Kinematic viscosity"), "nu",
             unidades.Diffusivity),
            (tr("pychemqt", "Thermal diffusivity"), "alfa",
             unidades.Diffusivity),
            (tr("pychemqt", "Surface tension"), "sigma",
             unidades.Tension),
            (tr("pychemqt", "Prandtl number"), "Prandt",
             unidades.Dimensionless),
            (tr("pychemqt", "Ideal gas Specific volume"),
             "v0", unidades.SpecificVolume),
            (tr("pychemqt", "Ideal gas Density"), "rho0",
             unidades.Density),
            (tr("pychemqt", "Ideal gas Specific enthalpy"),
             "h0", unidades.Enthalpy),
            (tr(
                "pychemqt", "Ideal gas Specific internal energy"), "u0",
                unidades.Enthalpy),
            (tr("pychemqt", "Ideal gas Specific entropy"),
             "s0", unidades.SpecificHeat),
            (tr(
                "pychemqt", "Ideal gas Specific Helmholtz free energy"),
                "a0", unidades.Enthalpy),
            (tr
             ("pychemqt", "Ideal gas Specific Gibbs free energy"), "g0",
             unidades.Enthalpy),
            (tr(
                "pychemqt", "Ideal gas Specific isobaric heat capacity"),
                "cp0", unidades.SpecificHeat),
            (tr(
                "pychemqt", "Ideal gas Specific isochoric heat capacity"),
                "cv0", unidades.SpecificHeat),
            (tr(
                "pychemqt", "Ideal gas heat capacities ratio"), "cp0_cv",
                unidades.Dimensionless),
            (tr(
                "pychemqt", "Ideal gas Isoentropic exponent"), "gamma0",
                unidades.Dimensionless)]
        return l

    @classmethod
    def propertiesName(cls):
        return [prop[0] for prop in cls.properties()]

    @classmethod
    def propertiesKey(cls):
        return [prop[1] for prop in cls.properties()]

    @classmethod
    def propertiesUnit(cls):
        return [prop[2] for prop in cls.properties()]

    @classmethod
    def _dictUnit(cls):
        d = {}
        for name, key, unit in cls.properties():
            d[key] = unit
        return d

    @classmethod
    def propertiesGlobal(cls):
        """List properties only availables for global stream, not defined by
        phase"""
        prop = ["T", "Tr", "P", "Pr", "x", "Hvap", "Svap", "v0", "rho0", "h0",
                "u0", "s0", "a0", "g0", "cp0", "cv0", "cp0_cv", "gamma0"]
        return prop

    @classmethod
    def propertiesPhase(cls):
        """List properties availables for single phase"""
        single = cls.propertiesGlobal()
        total = cls.propertiesKey()
        prop = []
        for p in total:
            if p not in single:
                prop.append(p)
        return prop

    def _fillCorriente(self, corriente):
        """Procedure to populate the corriente with the global advanced
        properties
        corriente: instance of corriente to populate"""
        for prop in self.propertiesGlobal():
            corriente.__setattr__(prop, self.__getattribute__(prop))

    def _writeGlobalState(self, corriente, state):
        """Procedure to populate a state dict with the global advanced
        properties
        corriente: instance of corriente to populate
        state: dict properties"""
        for prop in self.propertiesGlobal():
            state[prop] = corriente.__getattribute__(prop)

    def _readGlobalState(self, corriente, state):
        units = self._dictUnit()
        for prop in self.propertiesGlobal():
            if prop in ["K", "csat", "dpdt_sat", "cv2p", "chempot"]:
                value = [units[prop](p) for p in state[prop]]
            else:
                value = units[prop](state[prop])
            corriente.__setattr__(prop, value)

    def fillNone(self, fase):
        """Fill properties in null phase with a explicative msg"""
        fase._bool = False
        if self.x == 0:
            txt = tr("pychemqt", "Subcooled")
        elif self.Tr < 1 and self.Pr < 1:
            txt = tr("pychemqt", "Superheated")
        elif self.Tr == 1 and self.Pr == 1:
            txt = tr("pychemqt", "Critic point")
        elif self.Tr > 1 and self.Pr > 1:
            txt = tr("pychemqt", "Supercritical")
        else:
            txt = tr("pychemqt", "Undefined")

        for key in self.__class__.propertiesPhase():
            fase.__setattr__(key, txt)

    def writeStatetoJSON(self, state, fase):
        fluid = {}
        if self._bool:
            fluid["M"] = self.M
            fluid["v"] = self.v

            fluid["h"] = self.h
            fluid["s"] = self.s
            fluid["u"] = self.u
            fluid["a"] = self.a
            fluid["g"] = self.g

            fluid["cv"] = self.cv
            fluid["cp"] = self.cp
            fluid["cp/cv"] = self.cp_cv
            fluid["w"] = self.w

            fluid["Z"] = self.Z
            fluid["alfav"] = self.alfav
            fluid["kappa"] = self.kappa
            fluid["kappas"] = self.kappas

            fluid["mu"] = self.mu
            fluid["k"] = self.k
            fluid["nu"] = self.nu
            fluid["Prandt"] = self.Prandt

            fluid["alfa"] = self.alfa
            fluid["joule"] = self.joule
            fluid["deltat"] = self.deltat
            fluid["gamma"] = self.gamma

            fluid["alfap"] = self.alfap
            fluid["betap"] = self.betap
            fluid["fi"] = self.fi
            fluid["f"] = self.f

            fluid["volFlow"] = self.Q
            fluid["massFlow"] = self.caudalmasico
            fluid["molarFlow"] = self.caudalmolar
            fluid["fraction"] = self.fraccion
            fluid["massFraction"] = self.fraccion_masica
            fluid["massUnitFlow"] = self.caudalunitariomasico
            fluid["molarUnitFlow"] = self.caudalunitariomolar
        state[fase] = fluid

    def readStatefromJSON(self, fluid):
        if fluid:
            self._bool = True

            self.M = unidades.Dimensionless(fluid["M"])
            self.v = unidades.SpecificVolume(fluid["v"])
            self.rho = unidades.Density(1/self.v)

            self.h = unidades.Enthalpy(fluid["h"])
            self.s = unidades.SpecificHeat(fluid["s"])
            self.u = unidades.Enthalpy(fluid["u"])
            self.a = unidades.Enthalpy(fluid["a"])
            self.g = unidades.Enthalpy(fluid["g"])

            self.cv = unidades.SpecificHeat(fluid["cv"])
            self.cp = unidades.SpecificHeat(fluid["cp"])
            self.cp_cv = unidades.Dimensionless(fluid["cp/cv"])
            self.w = unidades.Speed(fluid["w"])

            self.Z = unidades.Dimensionless(fluid["Z"])
            self.alfav = unidades.InvTemperature(fluid["alfav"])
            self.kappa = unidades.InvPressure(fluid["kappa"])
            try:
                self.kappas = unidades.InvPressure(fluid["kappas"])
            except KeyError:
                self.kappas = unidades.InvPressure(0)

            self.mu = unidades.Viscosity(fluid["mu"])
            self.k = unidades.ThermalConductivity(fluid["k"])
            self.nu = unidades.Diffusivity(fluid["nu"])
            self.Prandt = unidades.Dimensionless(fluid["Prandt"])

            self.alfa = unidades.Diffusivity(fluid["alfa"])
            self.joule = unidades.TemperaturePressure(fluid["joule"])
            self.deltat = unidades.EnthalpyPressure(fluid["deltat"])
            self.gamma = unidades.Dimensionless(fluid["gamma"])

            self.alfap = unidades.Dimensionless(fluid["alfap"])
            self.betap = unidades.Dimensionless(fluid["betap"])
            try:
                self.fi = [unidades.Dimensionless(f) for f in fluid["fi"]]
                self.f = [unidades.Pressure(f) for f in fluid["f"]]
            except TypeError:
                self.fi = [unidades.Dimensionless(fluid["fi"])]
                self.f = [unidades.Pressure(fluid["f"])]


            self.Q = unidades.VolFlow(fluid["volFlow"])
            self.caudalmasico = unidades.MassFlow(fluid["massFlow"])
            self.caudalmolar = unidades.MolarFlow(fluid["molarFlow"])
            self.fraccion = [unidades.Dimensionless(x)
                             for x in fluid["fraction"]]
            self.fraccion_masica = [unidades.Dimensionless(x)
                                    for x in fluid["massFraction"]]
            self.caudalunitariomasico = [unidades.MassFlow(x)
                                         for x in fluid["massUnitFlow"]]
            self.caudalunitariomolar = [unidades.MolarFlow(x)
                                        for x in fluid["molarUnitFlow"]]

            self.rhoM = unidades.MolarDensity(self.rho/self.M)
            self.hM = unidades.MolarEnthalpy(self.h/self.M)
            self.sM = unidades.MolarSpecificHeat(self.s/self.M)
            self.uM = unidades.MolarEnthalpy(self.u/self.M)
            self.aM = unidades.MolarEnthalpy(self.a/self.M)
            self.gM = unidades.MolarEnthalpy(self.g/self.M)
            self.cvM = unidades.MolarSpecificHeat(self.cv/self.M)
            self.cpM = unidades.MolarSpecificHeat(self.cp/self.M)


class ThermoWater(Thermo):
    """Custom specified thermo instance to add special properties for water"""

    @classmethod
    def properties(cls):
        prop = Thermo.properties()[:]
        l = [
           (tr("pychemqt", "Dielectric constant"),
            "epsilon", unidades.Dimensionless),
           (tr("pychemqt", "Refractive index"),
            "n", unidades.Dimensionless)]
        for p in l:
            prop.insert(-11, p)
        return prop

    def writeStatetoJSON(self, state, fase):
        Thermo.writeStatetoJSON(self, state, fase)
        if self._bool:
            state[fase]["n"] = self.n
            state[fase]["epsilon"] = self.epsilon

    def readStatefromJSON(self, fluid):
        Thermo.readStatefromJSON(self, fluid)
        if fluid:
            self.epsilon = unidades.Dimensionless(fluid["epsilon"])
            self.n = unidades.Dimensionless(fluid["n"])


class ThermoAdvanced(Thermo):
    """Custom specified thermo instance to add special properties for advanced
    model as coolprop, refprop and meos"""

    @classmethod
    def properties(cls):
        prop = Thermo.properties()[:]
        l = [
            (tr(
                "pychemqt", "Isentropic temperature-pressure"),
                "betas", unidades.TemperaturePressure),
            (tr("pychemqt", "Gruneisen parameter"),
             "Gruneisen", unidades.Dimensionless),
            (tr("pychemqt", "2nd virial coefficient"),
             "virialB", unidades.SpecificVolume),
            (tr("pychemqt", "3er virial coefficient"),
             "virialC", unidades.SpecificVolume_square),
            ("(dp/dT)_rho", "dpdT_rho", unidades.PressureTemperature),
            ("(dp/drho)_T", "dpdrho_T", unidades.PressureDensity),
            ("(drho/dT)_P", "drhodT_P", unidades.DensityTemperature),
            ("(drho/dP)_T", "drhodP_T", unidades.DensityPressure),
            ("(dh/dT)_rho", "dhdT_rho", unidades.SpecificHeat),
            ("(dh/dP)_T", "dhdP_T", unidades.EnthalpyPressure),
            ("(dh/dT)_P", "dhdT_P", unidades.SpecificHeat),
            ("(dh/drho)_T", "dhdrho_T", unidades.EnthalpyDensity),
            ("(dh/dP)_rho", "dhdP_rho", unidades.EnthalpyPressure),
            (tr(
                "pychemqt", "Isothermal expansion coefficient"),
                "kt", unidades.Dimensionless),
            (tr(
                "pychemqt", "Isentropic expansion coefficient"),
                "ks", unidades.Dimensionless),
            (tr("pychemqt", "Adiabatic bulk modulus"),
             "Ks", unidades.Pressure),
            (tr("pychemqt", "Isothermal bulk modulus"),
             "Kt", unidades.Pressure),
            #        Z_rho     -   (Z-1) over the density, m³/kg
            (tr("pychemqt", "Internal pressure"),
             "IntP", unidades.Pressure),
            (tr(
                "pychemqt", "Negative reciprocal temperature"),
                "invT", unidades.InvTemperature),
            (tr("pychemqt", "Specific heat input"),
             "hInput", unidades.Enthalpy),
            (tr("pychemqt", "Dielectric constant"),
             "epsilon", unidades.Dimensionless)]

        for p in l:
            prop.insert(34, p)
        return prop

    @classmethod
    def propertiesGlobal(cls):
        """List properties only availables for global stream, not defined by
        phase"""
        prop = Thermo.propertiesGlobal()[:]
        prop.append("invT")
        return prop

    def writeStatetoJSON(self, state, fase):
        Thermo.writeStatetoJSON(self, state, fase)
        if self._bool:
            state[fase]["betas"] = self.betas
            state[fase]["Gruneisen"] = self.Gruneisen
            state[fase]["virialB"] = self.virialB
            state[fase]["virialC"] = self.virialC
            state[fase]["dpdT_rho"] = self.dpdT_rho
            state[fase]["dpdrho_T"] = self.dpdrho_T
            state[fase]["drhodT_P"] = self.drhodT_P
            state[fase]["drhodP_T"] = self.drhodP_T
            state[fase]["dhdT_rho"] = self.dhdT_rho
            state[fase]["dhdP_T"] = self.dhdP_T
            state[fase]["dhdT_P"] = self.dhdT_P
            state[fase]["dhdrho_T"] = self.dhdrho_T
            state[fase]["dhdP_rho"] = self.dhdP_rho
            state[fase]["kt"] = self.kt
            state[fase]["ks"] = self.ks
            state[fase]["Ks"] = self.Ks
            state[fase]["Kt"] = self.Kt
            state[fase]["IntP"] = self.IntP
            state[fase]["invT"] = self.invT
            state[fase]["hInput"] = self.hInput
            state[fase]["epsilon"] = self.epsilon

    def readStatefromJSON(self, fluid):
        Thermo.readStatefromJSON(self, fluid)
        if fluid:
            self.betas = unidades.TemperaturePressure(fluid["betas"])
            self.Gruneisen = unidades.Dimensionless(fluid["Gruneisen"])
            try:
                self.virialB = unidades.SpecificVolume(fluid["virialB"])
                self.virialC = unidades.SpecificVolume_square(fluid["virialC"])
            except KeyError:
                self.virialB = unidades.SpecificVolume(0)
                self.virialC = unidades.SpecificVolume_square(0)
            self.dpdT_rho = unidades.PressureTemperature(fluid["dpdT_rho"])
            self.dpdrho_T = unidades.PressureDensity(fluid["dpdrho_T"])
            self.drhodT_P = unidades.DensityTemperature(fluid["drhodT_P"])
            self.drhodP_T = unidades.DensityPressure(fluid["drhodP_T"])
            self.dhdT_rho = unidades.SpecificHeat(fluid["dhdT_rho"])
            self.dhdP_T = unidades.EnthalpyPressure(fluid["dhdP_T"])
            self.dhdT_P = unidades.SpecificHeat(fluid["dhdT_P"])
            self.dhdrho_T = unidades.EnthalpyDensity(fluid["dhdrho_T"])
            self.dhdP_rho = unidades.EnthalpyPressure(fluid["dhdP_rho"])
            self.kt = unidades.Dimensionless(fluid["kt"])
            self.ks = unidades.InvPressure(fluid["ks"])
            self.Ks = unidades.Pressure(fluid["Ks"])
            self.Kt = unidades.Pressure(fluid["Kt"])
            self.IntP = unidades.Pressure(fluid["IntP"])
            try:
                self.invT = unidades.InvTemperature(fluid["invT"])
            except KeyError:
                self.invT = unidades.InvTemperature(0)
            self.hInput = unidades.Enthalpy(fluid["hInput"])
            self.epsilon = unidades.Dimensionless(fluid["epsilon"])


class ThermoRefProp(ThermoAdvanced):
    """Custom specified thermo instance to add special properties for advanced
    model as coolprop, refprop and meos"""
    @classmethod
    def properties(cls):
        prop = ThermoAdvanced.properties()[:]
        l = [
            (tr("pychemqt", "Ideal Pressure"),
             "P0", unidades.Pressure),
            (tr("pychemqt", "Residual Pressure"),
             "P_Pideal", unidades.Pressure),
            (tr("pychemqt", "K value"),
             "K", unidades.Dimensionless),
            (tr(
                "pychemqt", "Heat Capacity along the saturation line"),
                "csat", unidades.SpecificHeat),
            ("dP/dT [sat]", "dpdt_sat", unidades.PressureTemperature),
            (tr("pychemqt", "Cv two phases"),
             "cv2p", unidades.SpecificHeat),
            (tr("pychemqt", "Excess volume"),
             "vE", unidades.SpecificVolume),
            (tr("pychemqt", "Excess internal energy"),
             "uE", unidades.Enthalpy),
            (tr("pychemqt", "Excess enthalpy"),
             "hE", unidades.Enthalpy),
            (tr("pychemqt", "Excess entropy"),
             "sE", unidades.SpecificHeat),
            (tr("pychemqt", "Excess Helmholtz energy"),
             "aE", unidades.Enthalpy),
            (tr("pychemqt", "Excess Gibbs energy"),
             "gE", unidades.Enthalpy),
            (tr("pychemqt", "Residual pressure"),
             "pr", unidades.SpecificVolume),
            (tr("pychemqt", "Residual internal energy"),
             "ur", unidades.Enthalpy),
            (tr("pychemqt", "Residual enthalpy"),
             "hr", unidades.Enthalpy),
            (tr("pychemqt", "Residual entropy"),
             "sr", unidades.SpecificHeat),
            (tr("pychemqt", "Residual Helmholtz energy"),
             "ar", unidades.Enthalpy),
            (tr("pychemqt", "Residual Gibbs energy"),
             "gr", unidades.Enthalpy),
            (tr(
                "pychemqt", "Residual isobaric heat capacity"),
             "cpr", unidades.SpecificHeat),
            (tr(
                "pychemqt", "Residual isochoric heat capacity"),
             "cvr", unidades.SpecificHeat),
            (tr("pychemqt", "Supercompressibility factor"),
             "fpv", unidades.Dimensionless),
            (tr("pychemqt", "Chemical potential"),
             "chempot", unidades.Enthalpy),
            (tr("pychemqt", "Fourth virial coefficient"),
             "virialD", unidades.Dimensionless),
            (tr(
                "pychemqt", "Second acoustic virial coefficient"),
             "virialBa", unidades.SpecificVolume),
            (tr(
                "pychemqt", "Third acoustic virial coefficient"),
             "virialCa", unidades.SpecificVolume_square),
            ("dC/dT", "dCdt", unidades.Dimensionless),
            ("d²C/dT²", "dCdt2", unidades.Dimensionless),
            ("dB/dT", "dBdt", unidades.Dimensionless),
            ("b12", "b12", unidades.SpecificVolume),
            (tr("pychemqt", "Critical flow factor"),
             "cstar", unidades.Dimensionless)]

        for p in l:
            prop.append(p)
        return prop

    @classmethod
    def propertiesGlobal(cls):
        """List properties only availables for global stream, not defined by
        phase"""
        prop = ThermoAdvanced.propertiesGlobal()
        new = ["P0", "P_Pideal", "K", "csat", "dpdt_sat", "cv2p", "vE", "uE",
               "hE", "sE", "aE", "gE", "pr", "ur", "hr", "sr", "ar", "gr",
               "cpr", "cvr", "fpv", "chempot", "b12", "cstar"]
        for p in new:
            prop.append(p)
        return prop

    def writeStatetoJSON(self, state, fase):
        ThermoAdvanced.writeStatetoJSON(self, state, fase)
        if self._bool:
            state[fase]["virialD"] = self.virialD
            state[fase]["virialBa"] = self.virialBa
            state[fase]["virialCa"] = self.virialCa
            state[fase]["dCdt"] = self.dCdt
            state[fase]["dCdt2"] = self.dCdt2
            state[fase]["dBdt"] = self.dBdt

    def readStatefromJSON(self, fluid):
        ThermoAdvanced.readStatefromJSON(self, fluid)
        if fluid:
            self.virialD = unidades.Dimensionless(fluid["virialD"])
            self.virialBa = unidades.SpecificVolume(fluid["virialBa"])
            self.virialCa = unidades.SpecificVolume_square(fluid["virialCa"])
            self.dCdt = unidades.Dimensionless(fluid["dCdt"])
            self.dCdt2 = unidades.Dimensionless(fluid["dCdt2"])
            self.dBdt = unidades.Dimensionless(fluid["dBdt"])
