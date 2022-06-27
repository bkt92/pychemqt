#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2022, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.



.. include:: drag.rst
'''


from math import exp, log, log10, tanh

from lib.utilities import refDoc


__doi__ = {
    1:
        {"autor": "Barati, R., Neyshabouri, S.A.A.S, Ahmadi, G.",
         "title": "Development of Empirical Models with High Accuracy for "
                  "Estimation of Drag Coefficient of Flow around a Smooth "
                  "Sphere: An Evolutionary Approach",
         "ref": "Powder Technology 257 (2014) 11-19",
         "doi": "10.1016/j.powtec.2014.02.045"},
    2:
        {"autor": "Clift, R., Grace, J.R., Weber, M.E.",
         "title": "Bubbles, Drops, and Particles",
         "ref": "Academic Press, 1978.",
         "doi": ""},
    3:
        {"autor": "Ceylan, K., Altunbaş, A., Kelbaliyev, G.",
         "title": "A New Model for Estimation of Drag Force in the Flow of "
                  "Newtonian Fluids around Rigid or Deformable Particles",
         "ref": "Powder Technology 119 (2001) 250-56",
         "doi": "10.1016/s0032-5910(01)00261-3"},
    4:
        {"autor": "Almedeij, J.",
         "title": "Drag Coefficient of Flow around a Sphere: Matching "
                  "Asymptotically the Wide Trend",
         "ref": "Powder Technology 186(3) (2008) 218-223",
         "doi": "10.1016/j.powtec.2007.12.006"},
    5:
        {"autor": "Morrison, F.A.",
         "title": "An Introduction to Fluid Mechanics.",
         "ref": "Cambridge University Press, 2013.",
         "doi": ""},
    6:
        {"autor": "Morsi, S.A., Alexander, A.J.",
         "title": "An Investigation of Particle Trajectories in Two-Phase "
                  "Flow Systems",
         "ref": "J. Fluid Mechanics 55(2) (1972) 193-208",
         "doi": "10.1017/S0022112072001806"},
    7:
        {"autor": "Brown, P.P., Lawler, D.F.",
         "title": "Sphere Drag and Settling Velocity Revisited",
         "ref": "J. Env. Eng. 129(3) (2003) 222-231",
         "doi": "10.1061/(ASCE)0733-9372(2003)129:3(222)"},
    8:
        {"autor": "Khan, A.R., Richardson, J.F.",
         "title": "The Resistance to Motion of a Solid Sphere in a Fluid.",
         "ref": "Chem. Eng. Comm. 62 (1987) 135-150",
         "doi": "10.1080/00986448708912056"},
    9:
        {"autor": "Flemmer, R.L.C., Banks, C.L.",
         "title": "On the Drag Coefficient of a Sphere",
         "ref": "Powder Technology 48(3) (1986) 217-221.",
         "doi": "10.1016/0032-5910(86)80044-4"},
    # 30:
        # {"autor": "",
         # "title": "",
         # "ref": "",
         # "doi": ""},
}


@refDoc(__doi__, [1])
def Barati(Re, extended=False):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [1]_.

    For Re < 2e5

    .. math::
        \begin{align*}
        C_d = 5.4856·10^9\tanh(4.3774\times10^{-9}/Re)
        + 0.0709\tanh(700.6574/Re) \\
        {} + 0.3894\tanh(74.1539/Re) - 0.1198\tanh(7429.0843/Re) \\
        {} + 1.7174\tanh[9.9851/(Re+2.3384)] + 0.4744
        \end{align*}

    For 2e5 <= Re < 1e6

    .. math::
        \begin{align*}
        C_d = 8·10^{-6}\left[(Re/6530)^2+\tanh(Re) - 8\ln(Re)/\ln(10)\right] \\
        {} - 0.4119\exp(-2.08x10^{43}/[Re + Re^2]^4) \\
        {} - 2.1344\exp(-{\left[\ln(Re^2 + 10.7563)/\ln(10)\right]^2
        + 9.9867}/Re) \\
        {} + 0.1357\exp(-[(Re/1620)^2 + 10370]/Re) \\
        {} - 8.5\times 10^{-3}\{2\ln[\tanh(\tanh(Re))]/\ln(10) - 2825.7162\}/Re
        \end{align*}

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]
    extended : boolean
        Use the extended version on all Re range of equation

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 1e6

    Examples
    --------
    Selected values from Table 6 in [1]_.

    >>> print("%0.2f" % Barati(0.002))
    12008.86
    >>> print("%0.2f" % Barati(0.002, extended=True))
    12034.71
    >>> print("%0.2f" % Barati(1000))
    0.47
    '''

    if not extended and Re < 2e5:
        # Eq 22
        Cd = 5.4856e9*tanh(4.3774e-9/Re) + 0.0709*tanh(700.6574/Re) \
            + 0.3894*tanh(74.1539/Re) - 0.1198*tanh(7429.0843/Re) \
            + 1.7174*tanh(9.9851/(Re+2.3384)) + 0.4744
    elif Re <= 1e6:
        # Eq 23
        Cd = 8e-6*((Re/6530)**2 + tanh(Re) - 8*log(Re)/log(10)) \
            - 0.4119*exp(-2.08e43/(Re+Re**2)**4) \
            - 2.1344*exp(-((log(Re**2 + 10.7563)/log(10))**2 + 9.9867)/Re) \
            + 0.1357*exp(-((Re/1620)**2 + 10370)/Re) \
            - 8.5e-3*(2*log(tanh(tanh(Re)))/log(10) - 2825.7162)/Re + 2.4795
    else:
        raise NotImplementedError("Input out of range 0 < Re ≤ 1e6")
    return Cd


@refDoc(__doi__, [2])
def Clift(Re):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [2]_.

    This method use different correlation for several ranges of Re, as describe
    in Table 5.2, pag 112

    .. math::
        C_d = \left\{ \begin{array}{ll}
        \frac{24}{Re} + \frac{3}{16} & \mbox{if $Re < 0.01$}\\
        \frac{24}{Re}(1 + 0.1315Re^{0.82 - 0.05w}) & \mbox{if $0.01 < Re < 20$}\\
        \frac{24}{Re}(1 + 0.1935Re^{0.6305}) & \mbox{if $20 < Re < 260$}\\
        10^{[1.6435 - 1.1242w + 0.1558w^2} & \mbox{if $260 < Re < 1500$}\\
        10^{[-2.4571 + 2.5558w - 0.9295w^2 + 0.1049w^3} &
        \mbox{if $1500 < Re < 1.2x10^4$}\\
        10^{[-1.9181 + 0.6370w - 0.0636w^2} &
        \mbox{if $1.2x10^4 < Re < 4.4x10^4$}\\
        10^{[-4.3390 + 1.5809w - 0.1546w^2} &
        \mbox{if $4.4x10^4 < Re < 3.38x10^5$}\\
        29.78 - 5.3w & \mbox{if $3.38x10^5 < Re < 4x10^5$}\\
        0.1w - 0.49 & \mbox{if $4x10^5 < Re < 10^6$}\\
        0.19w - \frac{8x10^4}{Re} & \mbox{if $10^6 < Re$}\end{array}\right.

    where :math:`w = \log_{10}{Re}`

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 6e6
    The last equation is based in Achenbach data and this reach 6e6 as maximum
    Reynolds number

    Examples
    --------
    There isn´t testing values but checking a value similar to Barati
    correlation would be enough

    >>> print("%0.0f" % Clift(0.002))
    12000
    >>> print("%0.2f" % Clift(1000))
    0.47
    '''
    w = log10(Re)

    if Re < 0.01:
        Cd = 3/16 + 24/Re
    elif Re < 20:
        Cd = 24/Re*(1 + 0.1315*Re**(0.82 - 0.05*w))
    elif Re < 260:
        Cd = 24/Re*(1 + 0.1935*Re**(0.6305))
    elif Re < 1500:
        Cd = 10**(1.6435 - 1.1242*w + 0.1558*w**2)
    elif Re < 1.2e4:
        Cd = 10**(-2.4571 + 2.5558*w - 0.9295*w**2 + 0.1049*w**3)
    elif Re < 4.4e4:
        Cd = 10**(-1.9181 + 0.6370*w - 0.0636*w**2)
    elif Re < 3.38e5:
        Cd = 10**(-4.3390 + 1.5809*w - 0.1546*w**2)
    elif Re < 4e5:
        Cd = 29.78 - 5.3*w
    elif Re < 1e6:
        Cd = 0.1*w - 0.49
    elif Re < 6e6:
        Cd = 0.19 - 8e4/Re
    else:
        raise NotImplementedError("Input out of range 0 < Re ≤ 6e6")
    return Cd


@refDoc(__doi__, [3])
def Ceylan(Re):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [3]_.

    .. math::
        \begin{align*}
        C_d = 1 - 0.5e^{0.182} + 10.11Re^{-2/3}e^{0.952Re^{-1/4}}
        - 0.03859Re^{-4/3}e^{1.30Re^{-1/2}} \\
        {} + 0.037\times10^{-4}Re e^{-0.125\times10^{-4}Re}
        -0.116\times10^{-10}Re^2 e^{-0.444\times10^{-5}Re}
        \end{align*}

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 1e6

    Examples
    --------
    Selected values from Table 2, pag 253

    # >>> print("%0.0f" % Ceylan(0.1))
    # 238
    # >>> print("%0.2f" % Ceylan(0.5))
    # 49.50
    # >>> print("%0.2f" % Ceylan(1e3))
    # 0.46

    >>> print("%0.2f" % Ceylan(1e6))
    0.26

    This correlation dont return the expected vaues in paper for low Reynolds
    numbers, possible a typo in paper
    '''
    if Re <= 0 or Re > 1e6:
        raise NotImplementedError("Input out of range 0 < Re ≤ 1e6")

    # Eq 15
    K1 = 1 - 0.5*exp(0.182) + 10.11*Re**(-2/3)*exp(0.952*Re**-0.25) \
        - 0.03859*Re**(-4/3)*exp(1.3*Re**(-0.5))
    K2 = 0.037e-4*Re*exp(-0.125e-4*Re) - 0.116e-10*Re**2*exp(-0.444e-5*Re)

    # Eq 14
    Cd = K1 + K2

    return Cd


@refDoc(__doi__, [4])
def Almedeij(Re):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [4]_.

    .. math::
        \begin{align*}
        C_d = \left(\frac{1}{(\phi_1 + \phi_2)^{-1} + (\phi_3)^{-1}} + \phi_4
        \right)^{0.1} \\
        {} \phi_1 = \left(\frac{24}{Re}\right)^{10} +
        \left(\frac{21}{Re^{0.67}}\right)^{10} +
        \left(\frac{4}{Re^{0.33}}\right)^{10} + 0.4^{10} \\
        {} \phi_2 = \frac{1}{\left[(0.148 Re^{0.11})^{-10} +
        (0.5)^{-10}\right]} \\
        {} \phi_3 = \left(\frac{1.57x10^8} {Re^{1.625}}\right)^{10} \\
        {} \phi_4 = \frac{1}{(6x10^{-17}Re^{2.63})^{-10} + (0.2)^{-10}}
        \end{align*}

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 1e6

    Examples
    --------
    There isn´t testing values but checking a value similar to Barati
    correlation would be enough

    >>> print("%0.0f" % Almedeij(0.002))
    12000
    >>> print("%0.2f" % Almedeij(1000))
    0.44
    '''
    if Re <= 0 or Re > 1e6:
        raise NotImplementedError("Input out of range 0 < Re ≤ 1e6")

    f1 = (24/Re)**10 + (21/Re**0.67)**10 + (4/Re**0.33)**10 + 0.4**10
    f2 = 1/((0.148*Re**0.11)**-10 + 0.5**-10)
    f3 = (1.57e8*Re**-1.625)**10
    f4 = 1/((6e-17*Re**2.63)**-10 + 0.2**-10)
    Cd = (1/((f1 + f2)**-1 + f3**-1) + f4)**0.1
    return Cd


@refDoc(__doi__, [5])
def Morrison(Re):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [5]_.

    .. math::
        C_d = \frac{24}{Re}+\frac{2.6 Re/5}{1+\left(\frac{Re}{5}\right)^{1.52}}
        + \frac{0.411 \left(\frac{Re}{263.000}\right)^{-7.94}}
        {1 + \left(\frac{Re}{263000}\right)^{-8}}
        + \frac{0.25 \left(\frac{Re}{10^6}\right)}
        {1+\left(\frac{Re}{10^6}\right)}

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 1e6

    Examples
    --------
    There isn´t testing values but checking a value similar to Barati
    correlation would be enough

    >>> print("%0.0f" % Morrison(0.002))
    12000
    >>> print("%0.2f" % Morrison(1000))
    0.48
    '''
    if Re <= 0 or Re > 1e6:
        raise NotImplementedError("Input out of range 0 < Re ≤ 1e6")

    Cd = 24/Re + 2.6*Re/5/(1 + (Re/5)**1.52) \
        + 0.411*(Re/263000)**-7.94/(1 + (Re/263000)**-8) \
        + 0.25*Re/1e6/(1+Re/1e6)
    return Cd


@refDoc(__doi__, [6])
def Morsi(Re):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [6]_.

    .. math::
        C_d = \left\{ \begin{array}{ll}
        \frac{24}{Re} & \mbox{if $Re<0.1$}\\
        \frac{22.73}{Re}+\frac{0.0903}{Re^2}+3.69 & \mbox{if $0.1<Re<1$}\\
        \frac{29.1667}{Re}-\frac{3.8889}{Re^2}+1.222 & \mbox{if $1<Re<10$}\\
        \frac{46.5}{Re}-\frac{116.67}{Re^2}+0.6167 & \mbox{if $10<Re<100$}\\
        \frac{98.33}{Re}-\frac{2778}{Re^2}+0.3644 & \mbox{if $100<Re<1000$}\\
        \frac{148.62}{Re}-\frac{4.75x10^4}{Re^2}+0.3570 &
        \mbox{if $1000<Re<5000$}\\
        \frac{-490.546}{Re}+\frac{57.87x10^4}{Re^2}+0.46 &
        \mbox{if $5000<Re<10000$}\\
        \frac{-1662.5}{Re}+\frac{5.4167x10^6}{Re^2}+0.5191 &
        \mbox{if $10000<Re<50000$}\end{array} \right.

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 5e5

    Examples
    --------
    Selected values from Table 1, pag 195

    >>> print("%0.2f" % Morsi(0.1))
    240.02
    >>> print("%0.2f" % Morsi(1000))
    0.46
    >>> print("%0.2f" % Morsi(5e4))
    0.49
    '''
    if 0 <= Re < 0.1:
        Cd = 24/Re
    elif Re < 1:
        Cd = 22.73/Re + 0.0903/Re**2 + 3.69
    elif Re < 10:
        Cd = 29.1667/Re - 3.8889/Re**2 + 1.222
    elif Re < 100:
        Cd = 46.5/Re - 116.67/Re**2 + 0.6167
    elif Re < 1000:
        Cd = 98.33/Re - 2778/Re**2 + 0.3644
    elif Re < 5000:
        Cd = 148.62/Re - 4.75e4/Re**2 + 0.357
    elif Re < 10000:
        Cd = -490.546/Re + 57.87e4/Re**2 + 0.46
    elif Re <= 50000:
        Cd = -1662.5/Re + 5.4167e6/Re**2 + 0.5191
    else:
        raise NotImplementedError("Input out of range 0 < Re < 5e5")
    return Cd


@refDoc(__doi__, [8, 7])
def Khan(Re, improved=True):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [8]_ including the improve in [7]_.

    Original correlation:

    .. math::
        C_d = (2.25Re^{-0.31} + 0.36Re^{0.06})^{3.45}

    Brown-Lawler improved version:

    .. math::
        C_d = (2.49Re^{-0.328} + 0.34Re^{0.067})^{3.18}


    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]
    improved : boolean
        Use the improved version from Brown-Lawler

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 3e5

    Examples
    --------
    There isn´t testing values but checking a value similar to Barati
    correlation would be enough

    >>> print("%0.2f" % Khan(1000))
    0.49
    '''
    if Re <= 0 or Re > 3e5:
        raise NotImplementedError("Input out of range 0 < Re ≤ 3e5")

    if improved:
        Cd = (2.49*Re**-0.328 + 0.34*Re**0.067)**3.18
    else:
        # Eq 15a
        Cd = (2.25*Re**-0.31 + 0.36*Re**0.06)**3.45

    return Cd


def Flemmer(Re, improved=True):
    r'''Calculates drag coefficient of a smooth sphere using the method in
    [9]_ including the improve in [7]_.

    Original correlation:

    .. math::
        C_d = \frac{24}{Re}10^E

        E = 0.261Re^{0.369}-0.105^{0.431} - \frac{0.124}{1+(\log Re)^2}

    Brown-Lawler improved version:

    .. math::

        E = 0.383Re^{0.356}-0.207Re^{0.396} - \frac{0.143}{1+(\log Re)^2}

    Parameters
    ----------
    Re : float
        Reynolds number of the sphere, [-]
    improved : boolean
        Use the improved version from Brown-Lawler

    Returns
    -------
    Cd : float
        Drag coefficient [-]

    Notes
    -----
    Raise :class:`NotImplementedError` if Re isn't in range Re ≤ 3e5

    Examples
    --------
    There isn´t testing values but checking a value similar to Barati
    correlation would be enough

    >>> print("%0.2f" % Flemmer(0.1))
    247.90
    >>> print("%0.2f" % Flemmer(1000))
    0.45
    >>> print("%0.2f" % Flemmer(5e4))
    0.48
    '''
    if Re <= 0 or Re > 3e5:
        raise NotImplementedError("Input out of range 0 < Re ≤ 3e5")

    if improved:
        E = 0.383*Re**0.356 - 0.207*Re**0.396 - 0.143/(1 + (log10(Re))**2)
    else:
        E = 0.261*Re**0.369 - 0.105*Re**0.431 - 0.124/(1 + (log10(Re))**2)

    return 24/Re*10**E


_all = Barati, Clift, Ceylan, Almedeij, Morrison, Morsi, Khan, Flemmer
