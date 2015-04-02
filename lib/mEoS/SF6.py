#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.meos import MEoS
from lib import unidades


class SF6(MEoS):
    """Multiparameter equation of state for sulfur hexafluoride"""
    name = "sulfur hexafluoride"
    CASNumber = "2551-62-4"
    formula = "SF6"
    synonym = ""
    rhoc = unidades.Density(742.297457)
    Tc = unidades.Temperature(318.7232)
    Pc = unidades.Pressure(3754.983, "kPa")
    M = 146.0554192  # g/mol
    Tt = unidades.Temperature(223.555)
    Tb = unidades.Temperature(204.9)
    f_acent = 0.21
    momentoDipolar = unidades.DipoleMoment(0.0, "Debye")
    # id = 953
    id = 1
    _Tr = unidades.Temperature(304.013497)
    _rhor = unidades.Density(747.815849)
    _w = 0.181815238

    CP1 = {"ao": 4.,
           "an": [], "pow": [],
           "ao_exp": [3.66118232, 7.87885103, 3.45981679],
           "exp": [1.617282065*Tc, 2.747115139*Tc, 4.232907175*Tc],
           "ao_hyp": [], "hyp": []}

    CP2 = {"ao": 3.9837756784,
           "an": [], "pow": [],
           "ao_exp": [2.2181851010, -1.0921337374e1, 3.3102497939,
                      17.5189671483, 2.8903523803],
           "exp": [1114.38, 925.64, 499.26, 884.9, 1363.93],
           "ao_hyp": [], "hyp": []}

    CP3 = {"ao": -0.376915e-1/8.3143*146.05,
           "an": [0.305814e-2/8.3143*146.05, -0.237654e-5/8.3143*146.05],
           "pow": [1, 2],
           "ao_exp": [], "exp": [],
           "ao_hyp": [], "hyp": []}

    helmholtz1 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for sulfur hexafluoride of Guder and Wagner (2007)",
        "__doc__":  u"""Guder, C. and Wagner, W. "A Reference Equation of State for the Thermodynamic Properties of Sulfur Hexafluoride for Temperatures from the Melting Line to 625 K and Pressures up to 150 MPa," to be submitted to J. Phys. Chem. Ref. Data, 2007.""",
        "R": 8.314472,
        "cp": CP1,
        
        "Tmin": Tt, "Tmax": 625.0, "Pmax": 150000.0, "rhomax": 14.5, 
        "Pmin": 231.429, "rhomin": 12.632, 

        "nr1": [.54958259132835, -.87905033269396, -.84656969731452,
                .27692381593529, -.49864958372345e01, .48879127058055e01,
                .36917081634281e-1, .37030130305087e-3, .39389132911585e-1,
                .42477413690006e-3],
        "d1": [1, 1, 1, 2, 2, 2, 3, 3, 4, 6],
        "t1": [0.125, 1.25, 1.875, 0.125, 1.5, 1.625, 1.5, 5.625, 0.625, 0.25],

        "nr2": [-.24150013863890e-1,  .59447650642255e-1, -.38302880142267,
                .32606800951983, -.29955940562031e-1, -.86579186671173e-1,
                .41600684707562e01, -.41398128855814e01, -.55842159922714,
                .56531382776891,  .82612463415545e-2, -.10200995338080e-1],
        "d2": [1, 2, 2, 2, 3, 6, 2, 2, 4, 4, 2, 2],
        "t2": [6., 0.25, 4.75, 5.375, 5.875, 2., 5.875, 6., 5.625, 5.75, 0., 0.5],
        "c2": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3],
        "gamma2": [1]*12,

        "nr3": [-.21662523861406e-1, .34650943893908e-1, -.28694281385812e-1,
                .84007238998053e-2, -.26969359922498, .90415215646344e01,
                -.37233103557977e01, -.27524670823704e04, .57711861697319e04,
                -.30234003119748e04, .22252778435360e07, -.23056065559032e07,
                .63918852944475e07, -.60792091415592e07],
        "d3": [1, 3, 4, 1, 1, 4, 3, 4, 4, 4, 1, 1, 3, 3],
        "t3": [4, 1, 3, 2, 4, 3, 4, 1, 2, 3, 3, 4, 3, 4],
        "alfa3": [10, 10, 10, 10, 11, 25, 30, 30, 30, 30, 30, 30, 30, 30, ],
        "beta3": [150, 150, 150, 150, 225, 300, 350, 350, 350, 350, 400, 400,
                  400, 400],
        "gamma3": [1.13, 1.13, 1.13, 1.16, 1.19, 1.19, 1.16, 1.16, 1.16, 1.16,
                   1.22, 1.22, 1.22, 1.22],
        "epsilon3": [0.85, 0.85, 0.85, 0.85, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}

    helmholtz2 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for sulfur hexafluoride of de Reuck et al. (1991)",
        "__doc__":  u"""de Reuck, K.M., Craven, R.J.B., and Cole, W.A., "Report on the Development of an Equation of State for Sulphur Hexafluoride," IUPAC Thermodynamic Tables Project Centre, London, 1991.""",
        "R": 8.31448,
        "cp": CP2,
        
        "Tmin": Tt, "Tmax": 525.0, "Pmax": 55000.0, "rhomax": 12.7, 
        "Pmin": 224.36, "rhomin": 12.677, 

        "nr1": [0.26945570453, -0.554046585076, -0.929624636454, 0.505661081063,
                -0.683495847809, 0.579161832426, -0.122636218956,
                -0.260339227668e-1, 0.222201648687e-1, -0.118992341472e-2,
                0.292000609763e-2, -0.243315775571e-2, 0.689778297550e-3],
        "d1": [1, 1, 1, 2, 2, 2, 3, 4, 5, 10, 10, 10, 10],
        "t1": [0, 1.5, 2, 0, 1, 2, 0, 2, 0, 0.5, 1, 1.5, 2],

        "nr2": [-0.147585329235e1, 0.275952303526e1, -0.142721418498e1,
                0.598794196648e-1, 0.219991168025e-2, 0.746554473361e-2,
                0.345233637389e-2, -0.253226231963e-1, 0.433906886402e-1,
                -0.249349699078e-1, 0.338560952242e-2, 0.539985899700e-3],
        "d2": [2, 2, 2, 3, 7, 7, 9, 4, 4, 4, 6, 4],
        "t2": [3, 4, 5, 5, 1, 5, 1, 9, 14, 24, 24, 9],
        "c2": [2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 6],
        "gamma2": [1]*12}

    helmholtz3 = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for sulfur hexafluoride of Span and Wagner (2003)",
        "__doi__": {"autor": "Span, R., Wagner, W.",
                    "title": "Equations of state for technical applications. II. Results for nonpolar fluids.", 
                    "ref": "Int. J. Thermophys. 24 (2003), 41 – 109.",
                    "doi": "10.1023/A:1022310214958"}, 
        "__test__": """
            >>> st=SF6(T=700, rho=200, eq=2)
            >>> print "%0.4f %0.3f %0.4f" % (st.cp0.kJkgK, st.P.MPa, st.cp.kJkgK)
            0.9671 8.094 0.9958
            >>> st2=SF6(T=750, rho=100, eq=2)
            >>> print "%0.2f %0.5f" % (st2.h.kJkg-st.h.kJkg, st2.s.kJkgK-st.s.kJkgK)
            52.80 0.10913
            """, # Table III, Pag 46

        "R": 8.31451,
        "cp": CP2,
        
        "Tmin": Tt, "Tmax": 600.0, "Pmax": 100000.0, "rhomax": 12.65, 
        "Pmin": 221.22, "rhomin": 12.645, 

        "nr1": [0.12279403e1, -0.33035623e1, 0.12094019e1, -0.12316,
                0.11044657, 0.32952153e-3],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.27017629, -0.62910351e-1, -0.3182889, -0.99557419e-1,
                -0.36909694e-1, 0.19136427e-1],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*7}

    helmholtz4 = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for sulfur hexafluoride of Polt et al. (1992)",
        "__doi__": {"autor": "Polt, A., Platzer, B., and Maurer, G.",
                    "title": "Parameter der thermischen Zustandsgleichung von Bender fuer 14 mehratomige reine Stoffe", 
                    "ref": "Chem. Technik 22(1992)6 , 216/224",
                    "doi": ""}, 
        "R": 8.3143,
        "cp": CP3,
        "ref": "NBP", 
        
        "Tmin": Tt, "Tmax": 523.0, "Pmax": 40000.0, "rhomax": 13.133, 
        "Pmin": 236.73, "rhomin": 12.712, 

        "nr1": [0.131111896375, -0.792338803106, 0.580899809209,
                0.153233600406e1, -0.485096079094e1, 0.482411603806e1,
                -0.311285647219e1, 0.442141211276, 0.206313183222,
                -0.372305169645, 0.443536383059, -0.476354850910e-1,
                0.116313319336, 0.570240883234e-1, -0.152963195118,
                0.259842094503e-1],
        "d1": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5],
        "t1": [3, 4, 5, 0, 1, 2, 3, 4, 0, 1, 2, 0, 1, 0, 1, 1],

        "nr2": [-0.131111896375, 0.792338803106, -0.580899809209,
                -0.744763581796, 0.204368923925e1, -0.129335324120e1],
        "d2": [0, 0, 0, 2, 2, 2],
        "t2": [3, 4, 5, 3, 4, 5],
        "c2": [2]*6,
        "gamma2": [1.32678063]*6}

    eq = helmholtz1, helmholtz2, helmholtz3, helmholtz4

    _surface = {"sigma": [0.05488, -1.62445e-3], "exp": [1.289, 1.799]}
    _melting = {"eq": 1, "Tref": Tt, "Pref": 0.48475e-4,
                "Tmin": Tt, "Tmax": 800.0,
                "a1": [1., -30.0468473, 30.0468473, 359.771253, -359.771253],
                "exp1": [0, -20., 0, 3.25, 0],
                "a2": [], "exp2": [], "a3": [], "exp3": []}
    _sublimation = {"eq": 2, "Tref": Tt, "Pref": 231.429,
                    "Tmin": Tt, "Tmax": Tt,
                    "a1": [-11.6942141, 11.6942141], "exp1": [-1.07, 0],
                    "a2": [], "exp2": [], "a3": [], "exp3": []}
    _vapor_Pressure = {
        "eq": 6,
        "ao": [-7.09634642, 1.676662, -2.3921599, 5.86078302, -9.02978735],
        "exp": [2.0, 3.0, 5.0, 8.0, 9.0]}
    _liquid_Density = {
        "eq": 6,
        "ao": [2.31174688, -1.12912486, -1.439347, 0.282489982],
        "exp": [1.065, 1.5, 4., 5.]}
    _vapor_Density = {
        "eq": 6,
        "ao": [23.68063442, 0.513062232, -24.4706238, -4.6715244, -1.7536843,
               -6.65585369],
        "exp": [1.044, 0.5, 1.0, 2.0, 8.0, 17.]}
