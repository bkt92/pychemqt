#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
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
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


###############################################################################
# Plot library with all matplotlib functionality
###############################################################################


from matplotlib import rcParams, rcdefaults, style
from matplotlib.backends import backend_qtagg
from matplotlib.colors import to_rgb
from matplotlib.figure import Figure
from numpy import arange

from lib.config import Preferences
from tools.qt import QtWidgets, tr
from UI.widgets import ColorSelector, LineStyleCombo, MarkerCombo


class PlotWidget(backend_qtagg.FigureCanvasQTAgg):
    """QWidget with matplotlib integration"""
    def __init__(self, dim=2, width=15, height=5, dpi=100, parent=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)

        self.dim = dim
        self.setParent(parent)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding)

        if dim == 2:
            self.ax = self.fig.add_subplot(111)

        else:
            self.ax = self.fig.add_subplot(projection="3d")
            self.ax.mouse_init(rotate_btn=1, zoom_btn=2)

    def plot(self, *args, **kwargs):
        """Direct accesst to ax plot procedure"""
        self.ax.plot(*args, **kwargs)

    def savePNG(self):
        """Save chart image to png file"""
        fmt = "Portable Network Graphics (*.png)"
        fname, ext = QtWidgets.QFileDialog.getSaveFileName(
            self,
            tr("pychemqt", "Save chart to file"),
            "./", fmt)
        if fname and ext == fmt:
            if fname.split(".")[-1] != "png":
                fname += ".png"
            self.fig.savefig(fname, facecolor='#fafafa')

    # def plot_3D(self, labels, xdata, ydata, zdata, config=None):
        # """Método que dibuja la matriz de datos"""
        # self.ax.clear()
        # self.data = {"x": xdata[0], "y": ydata[:, 0], "z": zdata}

        # if config and config.getboolean("MEOS", "surface"):
            # self.ax.plot_surface(xdata, ydata, zdata, rstride=1, cstride=1)
        # else:
            # self.ax.plot_wireframe(xdata, ydata, zdata, rstride=1, cstride=1)

        # self.ax.set_xlabel(labels[0])
        # self.ax.set_ylabel(labels[1])
        # self.ax.set_zlabel(labels[2])
        # self.ax.mouse_init(rotate_btn=1, zoom_btn=2)


class PlotDialog(QtWidgets.QDialog):
    """QDialog including Plotwidget, navigationtoolbar and a button to close"""
    def __init__(self, accept=False, cancel=True, parent=None):
        super().__init__(parent)
        gridLayout = QtWidgets.QGridLayout(self)

        self.plot = PlotWidget()
        gridLayout.addWidget(self.plot, 1, 1, 1, 2)
        self.toolbar = backend_qtagg.NavigationToolbar2QT(self.plot, self.plot)
        gridLayout.addWidget(self.toolbar, 2, 1)
        btonBox = QtWidgets.QDialogButtonBox()
        if accept:
            btonBox.addButton(QtWidgets.QDialogButtonBox.StandardButton.Ok)
            btonBox.accepted.connect(self.accept)
        if cancel:
            btonBox.addButton(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            btonBox.rejected.connect(self.reject)
        btonBox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                              QtWidgets.QSizePolicy.Policy.Maximum)
        gridLayout.addWidget(btonBox, 2, 2)

    def addText(self, *args, **kwargs):
        """Direct access to ax text procedure"""
        self.plot.ax.text(*args, **kwargs)

    def addData(self, *args, **kwargs):
        """Direct access to ax plot procedure"""
        self.plot.ax.plot(*args, **kwargs)


class ConfPlot(QtWidgets.QDialog):
    """Matplotlib configuration"""

    RCParams = {
        # Dict with options, the keys are the keyword matplotlib
        # Each option must define:
        #   - tooltip for widget with a tiny explanation
        #   - Widget class to use
        #   - Optional parameters
        #       - QComboBox: options to populate widget
        #       - QSpinBox: two values for define range (default 0-1)
        #       - QDoubleSpinBox: two values for define range (default 0-1),
        #           one more to define step (default 0.01 for range 0-1 or 1 in
        #           other cases) and one more for define decimals (default 2)

      "axes.facecolor": (
        tr("pychemqt", "Axes background color"),
        ColorSelector),
      "axes.edgecolor": (
        tr("pychemqt", "Axes edge color"),
        ColorSelector),
      "axes.linewidth": (
        tr("pychemqt", "Edge line width"),
        QtWidgets.QDoubleSpinBox, 0, 5, 0.1, 1),
      "axes.grid": (
        tr("pychemqt", "Display grid or not"),
        QtWidgets.QCheckBox),
      "axes.grid.axis": (
        tr(
          "pychemqt", "Which axis the grid should apply to"),
        QtWidgets.QComboBox, "both", "x", "y"),
      "axes.grid.which": (
        tr(
          "pychemqt", "Grid lines at {major, minor, both} ticks"),
        QtWidgets.QComboBox, "both", "major", "minor"),
      "axes.titlelocation": (
        tr("pychemqt", "Alignment of the title"),
        QtWidgets.QComboBox, "left", "right", "center"),
      "axes.titlesize": (
        tr(
          "pychemqt", "Font size of the axes title"),
        QtWidgets.QComboBox, 'xx-small', 'x-small', 'small', 'medium',
        'large', 'x-large', 'xx-large'),
      "axes.titleweight": (
        tr("pychemqt", "Font weight of title"),
        QtWidgets.QComboBox, "normal", "bold"),
      "axes.titlecolor": (
        tr("pychemqt", "Color of axes title"),
        ColorSelector),
      "axes.titley": (
        tr(
          "pychemqt", "Position title (axes relative units)"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "axes.titlepad": (
        tr(
          "pychemqt", "Pad between axes and title in points"),
        QtWidgets.QSpinBox, 0, 20),
      "axes.labelsize": (
        tr(
          "pychemqt", "Font size of the x and y labels"),
        QtWidgets.QComboBox, 'xx-small', 'x-small', 'small', 'medium',
        'large', 'x-large', 'xx-large'),
      "axes.labelpad": (
        tr(
          "pychemqt", "Pad between label and axis"),
        QtWidgets.QSpinBox, 0, 20),
      "axes.labelweight": (
        tr(
          "pychemqt", "Weight of the x and y labels"),
        QtWidgets.QComboBox, "normal", "bold"),
      "axes.labelcolor": (
        tr("pychemqt", "Axes label color"),
        ColorSelector),
      "axes.axisbelow": (
        tr(
          "pychemqt", "Draw axis gridlines and ticks"),
        QtWidgets.QComboBox, "True", "line", "False"),
      "axes.formatter.limits": (
        tr(
          "pychemqt", "Use scientific notation if log10 of the axis range is "
          "larger than this value"), QtWidgets.QSpinBox, 0, 10),
      "axes.formatter.use_locale": (
        tr(
          "pychemqt", "Format tick labels according to the user's locale"),
        QtWidgets.QCheckBox),
      "axes.formatter.use_mathtext": (
        tr(
          "pychemqt", "Use mathtext for scientific notation"),
        QtWidgets.QCheckBox),
      "axes.formatter.min_exponent": (
        tr(
          "pychemqt", "Minimum exponent to format in scientific notation"),
        QtWidgets.QSpinBox, 0, 10),
      "axes.formatter.useoffset": (
        tr(
          "pychemqt", "The tick label formatter will default to labeling "
          "ticks relative to an offset when the data range is small "
          "compared to the minimum absolute value of the data."),
        QtWidgets.QCheckBox),
      "axes.formatter.offset_threshold": (
        tr(
          "pychemqt", "When useoffset is True, the offset will be used when "
          "it can remove at least this number of significant digits from "
          "tick labels"),
        QtWidgets.QSpinBox, 0, 10),
      "axes.spines.left": (
        tr("pychemqt", "Display axis spines"),
        QtWidgets.QCheckBox),
      "axes.spines.bottom": (
        tr("pychemqt", "Display axis spines"),
        QtWidgets.QCheckBox),
      "axes.spines.top": (
        tr("pychemqt", "Display axis spines"),
        QtWidgets.QCheckBox),
      "axes.spines.right": (
        tr("pychemqt", "Display axis spines"),
        QtWidgets.QCheckBox),
      "axes.unicode_minus": (
        tr(
          "pychemqt", "Use Unicode for the minus symbol rather than hyphen"),
        QtWidgets.QCheckBox),
      "axes.xmargin": (
        tr("pychemqt", "X margin"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "axes.ymargin": (
        tr("pychemqt", "Y margin"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "axes.zmargin": (
        tr("pychemqt", "Z margin"),
        QtWidgets.QDoubleSpinBox, 0, 1),

      "axes3d.grid": (
        tr(
          "pychemqt", "Display grid on 3D axes"), QtWidgets.QCheckBox),

      "figure.titlesize": (
        tr(
          "pychemqt", "Size of the figure title"),
        QtWidgets.QComboBox, 'xx-small', 'x-small', 'small', 'medium',
        'large', 'x-large', 'xx-large'),
      "figure.titleweight": (
        tr(
          "pychemqt", "Weight of the figure title"),
        QtWidgets.QComboBox, "normal", "bold"),
      "figure.labelsize": (
        tr(
          "pychemqt", "Size of the figure label"),
        QtWidgets.QComboBox, 'xx-small', 'x-small', 'small', 'medium',
        'large', 'x-large', 'xx-large'),
      "figure.labelweight": (
        tr("pychemqt", "Weight of figure label"),
        QtWidgets.QComboBox, "normal", "bold"),
      # ("figure.figsize": (,     6.4, 4.8  # figure size in inches
      "figure.dpi": (
        tr("pychemqt", "Figure dots per inch"),
        QtWidgets.QSpinBox, 10,200),
      "figure.facecolor": (
        tr("pychemqt", "Figure face color"),
        ColorSelector),
      "figure.edgecolor": (
        tr("pychemqt", "Figure edge color"),
        ColorSelector),
      "figure.frameon": (
        tr("pychemqt", "Enable figure frame"),
        QtWidgets.QCheckBox),
      "figure.subplot.left": (
        tr(
          "pychemqt", "The left side of the subplots of the figure"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.subplot.right": (
        tr(
          "pychemqt", "The right side of the subplots of the figure"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.subplot.bottom": (
        tr(
          "pychemqt", "The bottom of the subplots of the figure"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.subplot.top": (
        tr(
          "pychemqt", "The top of the subplots of the figure"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.subplot.wspace": (
        tr(
          "pychemqt", "Width reserved for space between subplots"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.subplot.hspace": (
        tr(
          "pychemqt", "Height reserved for space between subplots"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.autolayout": (
        tr(
          "pychemqt", "Automatically adjust subplot"), QtWidgets.QCheckBox),
      "figure.constrained_layout.h_pad": (
        tr(
          "pychemqt", "Padding around axes objects. Float representing"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.constrained_layout.w_pad": (
        tr(
          "pychemqt", "Padding around axes objects. Float representing"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.constrained_layout.hspace": (
        tr(
          "pychemqt", "Space between subplot groups. Float representing"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "figure.constrained_layout.wspace": (
        tr(
          "pychemqt", "Space between subplot groups. Float representing"),
        QtWidgets.QDoubleSpinBox, 0, 1),

      "font.family": (
        "", QtWidgets.QComboBox,
        "serif", "sans-serif", "cursive", "fantasy", "monospace"),
      "font.style": ("", QtWidgets.QComboBox, "normal", "italic", "oblique"),
      "font.variant": ("", QtWidgets.QComboBox, "normal", "small-caps"),
      "font.weight": ("", QtWidgets.QComboBox, "normal", "bold"),
      "font.stretch": (
        "", QtWidgets.QComboBox, "ultra-condensed", "extra-condensed",
        "condensed", "semi-condensed", "normal", "semi-expanded", "expanded",
        "extra-expanded", "ultra-expanded", "wider", "narrower"),
      "font.size": ("", QtWidgets.QDoubleSpinBox, 5, 20, 0.5, 1),

      "grid.color": (
        tr("pychemqt", "Grid color"),
        ColorSelector),
      "grid.linestyle": (
        tr("pychemqt", "Grid line style"),
        LineStyleCombo),
      "grid.linewidth": (
        tr(
        "pychemqt", "Grid line width in points"),
        QtWidgets.QDoubleSpinBox, 0, 5, 0.1, 1),
      "grid.alpha": (
        tr("pychemqt", "Grid lines transparency"),
        QtWidgets.QDoubleSpinBox, 0, 1),

      "hatch.linewidth": (
        tr("pychemqt", "Line width in points"),
        QtWidgets.QDoubleSpinBox, 0, 5, 0.1, 1),
      "hatch.color": (
        tr("pychemqt", "Hatch color"),
        ColorSelector),

      "legend.loc": (
        tr(
          "pychemqt", "Location of legend in axes"),
        QtWidgets.QComboBox, 'best', 'center', 'center left', 'center right',
        'lower center', 'lower left', 'lower right', 'right', 'upper center',
        'upper left', 'upper right'),
      "legend.frameon": (
        tr(
            "pychemqt", "Draw the legend on a background patch"),
        QtWidgets.QCheckBox),
      "legend.framealpha": (
        tr(
            "pychemqt", "Legend patch transparency"),
        QtWidgets.QDoubleSpinBox, 0, 1),
      "legend.facecolor": (
        tr("pychemqt", "Legend patch color"),
        ColorSelector),
      "legend.edgecolor": (
        tr(
            "pychemqt", "Background patch boundary color"), ColorSelector),
      "legend.fancybox": (
        tr(
          "pychemqt", "Use a rounded box for the legend background, else a "
          "rectangle"), QtWidgets.QCheckBox),
      "legend.shadow": (
        tr(
            "pychemqt", "Give background a shadow effect"),
        QtWidgets.QCheckBox),
      "legend.numpoints": (
        tr(
          "pychemqt", "Number of marker points in the legend line"),
        QtWidgets.QSpinBox, 1, 10),
      "legend.scatterpoints": (
        tr(
          "pychemqt", "Number of scatter points"),
        QtWidgets.QSpinBox, 1, 10),
      "legend.markerscale": (
        tr(
          "pychemqt", "Relative size of legend markers vs. original"),
        QtWidgets.QDoubleSpinBox, 0, 2, 0.1, 1),
      "legend.fontsize": ("", QtWidgets.QComboBox, 'xx-small', 'x-small',
                          'small', 'medium', 'large', 'x-large', 'xx-large'),
      "legend.labelcolor": ("", ColorSelector),
      "legend.title_fontsize": ("", QtWidgets.QComboBox, 'xx-small', 'x-small',
                                'small', 'medium', 'large', 'x-large', 'xx-large'),
      "legend.borderpad": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for border whitespace"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "legend.labelspacing": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for the vertical "
          "space between the legend entries"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "legend.handlelength": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for the length of "
          "the legend lines"), QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "legend.handleheight": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for the height of "
          "the legend handle"), QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "legend.handletextpad": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for the space "
          "between the legend line and legend text"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "legend.borderaxespad": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for the border "
          "between the axes and legend edge"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "legend.columnspacing": (
        tr(
          "pychemqt", "Dimensions as fraction of font size for column separation"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),

      "lines.linewidth": (
        tr("pychemqt", "Line width in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "lines.linestyle": (
        tr("pychemqt", "Line style"),
        LineStyleCombo),
      "lines.color": (
        tr("pychemqt", "Line color"),
        ColorSelector),
      "lines.marker": (
        tr("pychemqt", "Marker style"),
        MarkerCombo),
      "lines.markerfacecolor": (
        tr("pychemqt", "Marker face color"),
        ColorSelector),
      "lines.markeredgecolor": (
        tr("pychemqt", "Marker edge color"),
        ColorSelector),
      "lines.markeredgewidth": (
        tr(
          "pychemqt", "Line width around the marker symbol"),
        QtWidgets.QDoubleSpinBox, 0, 5, 0.1, 1),
      "lines.markersize": (
        tr("pychemqt", "Marker size, in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "lines.dash_joinstyle": ("", QtWidgets.QComboBox, "miter", "round", "bevel"),
      "lines.dash_capstyle": ("", QtWidgets.QComboBox, "butt", "round", "projecting"),
      "lines.solid_joinstyle": ("", QtWidgets.QComboBox, "miter", "round", "bevel"),
      "lines.solid_capstyle": ("", QtWidgets.QComboBox, "butt", "round", "projecting"),
      "lines.antialiased": (
        tr("pychemqt", "Render antialiased"),
        QtWidgets.QCheckBox),
      "lines.scale_dashes": ("", QtWidgets.QCheckBox),

      "patch.linewidth": (
        tr("pychemqt", "Edge width in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "patch.facecolor": (
        tr("pychemqt", "Patch face color"),
        ColorSelector),
      "patch.edgecolor": (
        tr("pychemqt", "Patch edge color"),
        ColorSelector),
      "patch.force_edgecolor": (
        tr("pychemqt", "Always use edgecolor"),
        QtWidgets.QCheckBox),
      "patch.antialiased": (
        tr("pychemqt", "Render patch antialiased"),
        QtWidgets.QCheckBox),

      "xtick.top": (
        tr(
          "pychemqt", "Draw ticks on the top side"), QtWidgets.QCheckBox),
      "xtick.bottom": (
        tr(
          "pychemqt", "Draw ticks on the bottom side"), QtWidgets.QCheckBox),
      "xtick.labeltop": (
        tr("pychemqt", "Draw label on the top"),
        QtWidgets.QCheckBox),
      "xtick.labelbottom": (
        tr("pychemqt", "Draw label on the bottom"),
        QtWidgets.QCheckBox),
      "xtick.major.size": (
        tr("pychemqt", "Major tick size in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "xtick.minor.size": (
        tr("pychemqt", "Minor tick size in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "xtick.major.width": (
        tr("pychemqt", "Major tick width in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "xtick.minor.width": (
        tr("pychemqt", "Minor tick width in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "xtick.major.pad": (
        tr(
          "pychemqt", "Distance to major tick label in points"),
        QtWidgets.QDoubleSpinBox, 0, 20, 0.1, 1),
      "xtick.minor.pad": (
        tr(
          "pychemqt", "Distance to the minor tick label in points"),
        QtWidgets.QDoubleSpinBox, 0, 20, 0.1, 1),
      "xtick.color": (
        tr("pychemqt", "Color of the ticks"),
        ColorSelector),
      "xtick.labelcolor": (
        tr(
          "pychemqt", "Color of the tick labels or inherit from xtick.color"),
        ColorSelector),
      "xtick.labelsize": (
        tr(
          "pychemqt", "Font size of the tick labels"),
        QtWidgets.QComboBox, 'xx-small', 'x-small', 'small', 'medium',
        'large', 'x-large', 'xx-large'),
      "xtick.direction": (
        tr("pychemqt", "Direction"),
        QtWidgets.QComboBox, "in", "out", "inout"),
      "xtick.minor.visible": (
        tr(
          "pychemqt", "Visibility of minor ticks on x-axis"),
        QtWidgets.QCheckBox),
      "xtick.major.top": (
        tr("pychemqt", "Draw x axis top major ticks"),
        QtWidgets.QCheckBox),
      "xtick.major.bottom": (
        tr("pychemqt", "Draw x axis bottom major ticks"),
        QtWidgets.QCheckBox),
      "xtick.minor.top": (
        tr("pychemqt", "Draw x axis top minor ticks"),
        QtWidgets.QCheckBox),
      "xtick.minor.bottom": (
        tr("pychemqt", "Draw x axis bottom minor ticks"),
        QtWidgets.QCheckBox),
      "xtick.alignment": (
        tr("pychemqt", "Alignment of ticks"),
        QtWidgets.QComboBox, "left", "center", "right"),

      "ytick.left": (
        tr("pychemqt", "Draw ticks on the left side"),
        QtWidgets.QCheckBox),
      "ytick.right": (
        tr("pychemqt", "Draw ticks on the right side"),
        QtWidgets.QCheckBox),
      "ytick.labelleft": (
        tr("pychemqt", "Draw label on the left"),
        QtWidgets.QCheckBox),
      "ytick.labelright": (
        tr("pychemqt", "Draw label on the right"),
        QtWidgets.QCheckBox),
      "ytick.major.size": (
        tr("pychemqt", "Major tick size in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "ytick.minor.size": (
        tr("pychemqt", "Minor tick size in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "ytick.major.width": (
        tr("pychemqt", "Major tick width in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "ytick.minor.width": (
        tr("pychemqt", "Minor tick width in points"),
        QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "ytick.major.pad": (
        tr(
          "pychemqt", "Distance to major tick label in points"),
        QtWidgets.QDoubleSpinBox, 0, 20, 0.1, 1),
      "ytick.minor.pad": (
        tr(
          "pychemqt", "Distance to the minor tick label in points"),
        QtWidgets.QDoubleSpinBox, 0, 20, 0.1, 1),
      "ytick.color": (
        tr("pychemqt", "Color of the ticks"),
        ColorSelector),
      "ytick.labelcolor": (
        tr(
          "pychemqt", "Color of the tick labels or inherit from ytick.color"),
        ColorSelector),
      "ytick.labelsize": (
        tr("pychemqt", "Font size of the tick labels"),
        QtWidgets.QComboBox, 'xx-small', 'x-small', 'small', 'medium',
        'large', 'x-large', 'xx-large'),
      "ytick.direction": (
        tr("pychemqt", "Direction"),
        QtWidgets.QComboBox, "in", "out", "inout"),
      "ytick.minor.visible": (
        tr(
          "pychemqt", "Visibility of minor ticks on y-axis"),
        QtWidgets.QCheckBox),
      "ytick.major.left": (
        tr("pychemqt", "Draw y axis left major ticks"),
        QtWidgets.QCheckBox),
      "ytick.major.right": (
        tr("pychemqt", "Draw y axis right major ticks"),
        QtWidgets.QCheckBox),
      "ytick.minor.left": (
        tr("pychemqt", "Draw y axis left minor ticks"),
        QtWidgets.QCheckBox),
      "ytick.minor.right": (
        tr("pychemqt", "Draw y axis right minor ticks"),
        QtWidgets.QCheckBox),
      "ytick.alignment": (
        tr("pychemqt", "Alignment of ticks"),
        QtWidgets.QComboBox, 'bottom', 'baseline', 'center', 'center_baseline', 'top'),

      "xaxis.labellocation": (
        tr(
          "pychemqt", "Alignment of the xaxis label"),
        QtWidgets.QComboBox, "center", "left", "right"),
      "yaxis.labellocation": (
        tr(
         "pychemqt", "Alignment of the yaxis label"),
        QtWidgets.QComboBox, "center", "bottom", "top"),

      "savefig.dpi": (
        tr("pychemqt", "Figure dots per inch"),
        QtWidgets.QSpinBox, 0, 100),
      "savefig.facecolor": (
        tr("pychemqt", "Figure facecolor when saving"),
        ColorSelector),
      "savefig.edgecolor": (
        tr("pychemqt", "Figure edgecolor when saving"),
        ColorSelector),
      "savefig.format": (
        tr("pychemqt", "File format so save"),
        QtWidgets.QComboBox, "png", "ps", "pdf", "svg"),
      "savefig.bbox": ("", QtWidgets.QComboBox, "standard", "tight"),
      "savefig.pad_inches": (
        tr(
          "pychemqt", "Padding to be used, when bbox is set to 'tight'"),
          QtWidgets.QDoubleSpinBox, 0, 10, 0.1, 1),
      "savefig.transparent": (
        tr(
          "pychemqt", "Figures are saved with a transparent background"),
        QtWidgets.QCheckBox)
          }

    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QLabel(tr(
            "pychemqt", "Matplotlib Style:")), 1, 1)
        self.style = QtWidgets.QComboBox()
        layout.addWidget(self.style, 1, 2)
        self.style.addItem("default")
        for sty in style.available:
            self.style.addItem(sty)
        self.style.currentTextChanged.connect(self.updateStyle)

        self.customize = QtWidgets.QCheckBox(tr(
            "pychemqt", "Costomize Style:"))
        layout.addWidget(self.customize, 2, 1, 1, 3)
        self.tabRcParams = QtWidgets.QTabWidget()
        self.tabRcParams.setEnabled(False)
        layout.addWidget(self.tabRcParams, 3, 1, 1, 3)
        self.customize.toggled.connect(self.tabRcParams.setEnabled)
        self.customize.toggled.connect(self.updatePlot)

        tab = []
        tab_widgets = []
        for label, (tooltip, wdg, *opt) in sorted(self.RCParams.items()):
            title = label.split(".")[0]

            # Regroup tiny option in axes tab
            if title in ("xaxis", "yaxis", "axes3d"):
                title = "axes"

            # Add new tab if not exist
            if title not in tab:
                tab.append(title)
                tab_widgets.append(QtWidgets.QWidget())
                QtWidgets.QVBoxLayout(tab_widgets[-1])

            # Get index of current tab to add widget
            idx = tab.index(title)

            # Create widget with a horizontal layout to add label and
            # appropiate input widget
            rc_widget = QtWidgets.QWidget()
            lyt_wdg = QtWidgets.QHBoxLayout(rc_widget)
            lyt_wdg.addWidget(QtWidgets.QLabel(label, rc_widget))

            # Create the appropiate input widget as defined in rc dict
            if wdg == QtWidgets.QDoubleSpinBox:
                wdg = QtWidgets.QDoubleSpinBox()
                wdg.setRange(*opt[:2])
                if len(opt) >= 3:
                    wdg.setSingleStep(opt[2])
                if len(opt) == 4:
                    wdg.setDecimals(opt[3])
                elif opt[1] == 1 and opt[0] == 0:
                    wdg.setSingleStep(0.01)
                wdg.valueChanged.connect(self.updatePlot)
            elif wdg == QtWidgets.QSpinBox:
                wdg = QtWidgets.QSpinBox()
                wdg.setRange(*opt)
                wdg.valueChanged.connect(self.updatePlot)
            elif wdg == QtWidgets.QComboBox:
                wdg = QtWidgets.QComboBox()
                for value in opt:
                    wdg.addItem(value)
                wdg.currentIndexChanged.connect(self.updatePlot)
            elif wdg == LineStyleCombo:
                wdg = LineStyleCombo()
                wdg.currentIndexChanged.connect(self.updatePlot)
            elif wdg == MarkerCombo:
                wdg = MarkerCombo()
                wdg.currentIndexChanged.connect(self.updatePlot)
            elif wdg == ColorSelector:
                wdg = ColorSelector()
                wdg.valueChanged.connect(self.updatePlot)
            elif wdg == QtWidgets.QCheckBox:
                wdg = QtWidgets.QCheckBox()
                wdg.toggled.connect(self.updatePlot)

            wdg.setToolTip(tooltip)
            lyt_wdg.addWidget(wdg)
            lyt_wdg.addItem(QtWidgets.QSpacerItem(
                10, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Fixed))

            tab_widgets[idx].layout().addWidget(rc_widget)

        for title, wdg in zip(tab, tab_widgets):
            # Add a spacer item at end of each tabwidget
            wdg.layout().addItem(QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding))

            # Now when the widget is pupulate add the scrollArea
            scroll = QtWidgets.QScrollArea()
            scroll.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
            scroll.setWidget(wdg)
            self.tabRcParams.addTab(scroll, title)

        layout.addItem(QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding), 10, 1, 1, 3)

        if config.has_section("Plot"):
            self.style.setCurrentIndex(config.getint("Plot", 'style'))
            self.customize.setChecked(config.getboolean("Plot", 'customize'))

            for idx in range(self.tabRcParams.count()):
                tab = self.tabRcParams.widget(idx).widget()
                for parent_wdg in tab.children()[1:]:
                    label, wdg = parent_wdg.children()[1:]
                    if isinstance(wdg, QtWidgets.QDoubleSpinBox):
                        wdg.setValue(config.getfloat("Plot", label.text()))
                    elif isinstance(wdg, QtWidgets.QSpinBox):
                        if label.text() == "axes.formatter.limits":
                            # Convert saved value as tuple to integer
                            value = config.get("Plot", label.text())
                            value = -int(value.split(",")[0])
                            wdg.setValue(value)
                        else:
                            wdg.setValue(config.getint("Plot", label.text()))
                    elif isinstance(wdg, LineStyleCombo):
                        wdg.setCurrentText(config.get("Plot", label.text()))
                    elif isinstance(wdg, MarkerCombo):
                        wdg.setCurrentText(config.get("Plot", label.text()))
                    elif isinstance(wdg, QtWidgets.QComboBox):
                        wdg.setCurrentText(config.get("Plot", label.text()))
                    elif isinstance(wdg, QtWidgets.QCheckBox):
                        wdg.setChecked(config.getboolean("Plot", label.text()))
                    elif isinstance(wdg, ColorSelector):
                        wdg.setColor(config.get("Plot", label.text()))

        self.updatePlot()

    def updateStyle(self, textStyle):
        """Update rcParams with the new selected style and update plot"""
        rcdefaults()

        if textStyle != "default":
            rcParams.update(style.library[textStyle])

        self._setRcParams(rcParams)
        self.updatePlot()

    def updatePlot(self):
        """Update plot with the new configuration, global style or only a
        rcParams changed"""
        if self.customize.isChecked():
            textStyle = self._getRcParams()

        else:
            textStyle = self.style.currentText()

        self.plot(textStyle)

    def plot(self, textStyle):
        """Do the sample plot using the specified style confuguration, the
        style configuration can be a named matplotlib style or a dictionary
        with rc_params"""
        with style.context(textStyle):
            x = arange(-2, 8, .2)
            y = .1 * x ** 3 - x ** 2 + 3 * x + 2
            z = .01 * x ** 3 + x ** 2 - 3 * x - 2

            plot = PlotWidget(width=1, height=1)
            plot.plot(x, y, label="f(x)")
            plot.plot(x, z, label="g(x)")
            plot.ax.set_title("Function representation")
            plot.ax.set_xlabel("x")
            plot.ax.set_ylabel(r"$y=f\left(x\right)$")
            plot.ax.legend()
            self.layout().addWidget(plot, 9, 1, 1, 3)

    def _getRcParams(self):
        """Get rc parameters from widgets"""
        kw = {}
        for idx in range(self.tabRcParams.count()):
            tab = self.tabRcParams.widget(idx).widget()

            # The first children is always the layout used so we discard it
            for parent_wdg in tab.children()[1:]:
                label, wdg = parent_wdg.children()[1:]

                if isinstance(wdg, QtWidgets.QDoubleSpinBox):
                    # Correct value for axes.titley
                    if label.text() == "axes.titley" and value == 1.:
                        value = None
                    else:
                        value = wdg.value()
                elif isinstance(wdg, QtWidgets.QSpinBox):
                    # Correct value to matplotlib expected format
                    if label.text() == "axes.formatter.limits":
                        value = f"-{wdg.value()}, {wdg.value()}"
                    else:
                        value = wdg.value()
                elif isinstance(wdg, (LineStyleCombo, MarkerCombo)):
                    value = wdg.currentValue()
                elif isinstance(wdg, QtWidgets.QComboBox):
                    value = wdg.currentText()
                elif isinstance(wdg, QtWidgets.QCheckBox):
                    value = wdg.isChecked()
                elif isinstance(wdg, ColorSelector):
                    value = wdg.color.name()

                kw[label.text()] = value
        return kw

    def _setRcParams(self, rcparams):
        """Populate widgets with the dict rcparams given as parameter"""
        for idx in range(self.tabRcParams.count()):
            tab = self.tabRcParams.widget(idx).widget()
            for parent_wdg in tab.children()[1:]:
                label, wdg = parent_wdg.children()[1:]
                wdg.blockSignals(True)
                value = rcparams.get(label.text(), None)

                if isinstance(wdg, QtWidgets.QDoubleSpinBox):
                    # Correct default value
                    if label.text() == "axes.titley" and value is None:
                        value = 1.
                    if label.text() == "legend.framealpha" and value is None:
                        value = 0.8
                    wdg.setValue(value)
                elif isinstance(wdg, QtWidgets.QSpinBox):
                    # Correct default value
                    if label.text() == "savefig.dpi" and value == "figure":
                        value = rcparams["figure.dpi"]
                    if label.text() == "axes.formatter.limits":
                        value = -value[0]
                    wdg.setValue(int(value))
                elif isinstance(wdg, LineStyleCombo):
                    wdg.setCurrentValue(value)
                elif isinstance(wdg, MarkerCombo):
                    wdg.setCurrentValue(value)
                elif isinstance(wdg, QtWidgets.QComboBox):
                    # Do text manipulation for joinstyle enum
                    if label.text() in (
                            "lines.dash_joinstyle", "lines.solid_joinstyle"):
                        value = value.split(".")[-1]
                    # Do text manipulation for capstyle enum
                    if label.text() in (
                            "lines.dash_capstyle", "lines.solid_capstyle"):
                        value = value.split(".")[-1]
                    # Do text manipulation for font.family
                    if label.text() == "font.family":
                        value = value[0]
                    wdg.setCurrentText(str(value))
                elif isinstance(wdg, QtWidgets.QCheckBox):
                    wdg.setChecked(value)
                elif isinstance(wdg, ColorSelector):

                    # Correct auto and inherit values
                    if label.text() == "axes.titlecolor" and value == "auto":
                        value = rcparams["text.color"]
                    if label.text() == "legend.facecolor" and value == "inherit":
                        value = rcparams["axes.facecolor"]
                    if label.text() == "legend.edgecolor" and value == "inherit":
                        value = rcparams["axes.edgecolor"]
                    if label.text() == "xtick.labelcolor" and value == "inherit":
                        value = rcparams["xtick.color"]
                    if label.text() == "ytick.labelcolor" and value == "inherit":
                        value = rcparams["ytick.color"]
                    if label.text() == "savefig.facecolor" and value == "auto":
                        value = rcparams["figure.facecolor"]
                    if label.text() == "savefig.edgecolor" and value == "auto":
                        value = rcparams["figure.edgecolor"]
                    if label.text() == "lines.markeredgecolor" and value == "auto":
                        value = "#000000"
                    if label.text() == "lines.markerfacecolor" and value == "auto":
                        value = "C2"

                    # Get the RGB code of color to avoid the several color
                    # definition in matplotlib and its styles
                    r, g, b = to_rgb(value)

                    r = int(float(r)*255)
                    g = int(float(g)*255)
                    b = int(float(b)*255)
                    value = f"#{r:x}{g:x}{b:x}"

                    wdg.setColor(value)

                wdg.blockSignals(False)

    def value(self, config):
        """Update ConfigParser instance with the config"""
        if not config.has_section("Plot"):
            config.add_section("Plot")
        config.set("Plot", "style", str(self.style.currentIndex()))
        config.set("Plot", "customize", str(self.customize.isChecked()))

        for k, val in self._getRcParams().items():
            config.set("Plot", k, str(val))

        return config


# Load style defined in preferences
if Preferences.getboolean("Plot", 'customize'):
    rc = {}
    for key, (tip, widget, *args) in ConfPlot.RCParams.items():
        if widget == QtWidgets.QDoubleSpinBox:
            rc[key] = Preferences.getfloat("Plot", key)
        elif widget == QtWidgets.QSpinBox:
            if key == "axes.formatter.limits":
                rc[key] = Preferences.get("Plot", key)
            else:
                rc[key] = Preferences.getint("Plot", key)
        elif widget == QtWidgets.QCheckBox:
            rc[key] = Preferences.getboolean("Plot", key)
        else:
            rc[key] = Preferences.get("Plot", key)
    style.use(rc)
elif Preferences.getint("Plot", 'style') == 0:
    style.use("default")
else:
    style.use(style.available[Preferences.getint("Plot", 'style')-1])


if __name__ == "__main__":
    import os
    import sys
    from configparser import ConfigParser
    conf_dir = os.path.expanduser('~') + "/.pychemqt/"
    pychemqt_dir = os.environ["PWD"] + "/"
    app = QtWidgets.QApplication(sys.argv)

    conf = ConfigParser()
    conf.read(conf_dir+"pychemqtrc")
    dialogo = ConfPlot(conf)

    dialogo.show()
    sys.exit(app.exec())
