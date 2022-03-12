"""
Algobot GUI themes.
"""

from interface.palettes import bloomberg_palette, dark_palette, green_palette, light_palette, red_palette


def set_dark_mode(app, gui):
    """
    Switches interface to a dark theme.
    """
    app.setPalette(dark_palette())


def set_light_mode(app, gui):
    """
    Switches interface to a light theme.
    """
    app.setPalette(light_palette())


def set_bloomberg_mode(app, gui):
    """
    Switches interface to bloomberg theme.
    """
    app.setPalette(bloomberg_palette())
    for graph in gui.graphs:
        graph = graph['graph']
        graph.setBackground('k')


def set_bear_mode(app, gui):
    """
    Sets bear mode color theme. Theme is red and black mimicking a red day.
    """
    app.setPalette(red_palette())


def set_bull_mode(app, gui):

    app.setPalette(green_palette())
    for graph in gui.graphs:
        graph = graph['graph']
        graph.setBackground('k')