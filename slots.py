"""
Slots for Algobot GUI.
"""

from interface.utils import clear_table
from themes import set_bear_mode, set_bloomberg_mode, set_bull_mode, set_dark_mode, set_light_mode


def initiate_slots(app, gui):
    """
    Initiates all interface slots.
    """
    create_interface_slots(gui)
    create_conf_slots(app=app, gui=gui)


def create_interface_slots(gui):
    """
    Creates interface slots.
    """
    create_simulation_slots(gui)


def create_conf_slots(app, gui):
    gui.configuration.lightModeRadioButton.toggled.connect(lambda: set_light_mode(app, gui))
    gui.configuration.darkModeRadioButton.toggled.connect(lambda: set_dark_mode(app, gui))
    # gui.configuration.bloombergModeRadioButton.toggled.connect(lambda: set_bloomberg_mode(app, gui))
    # gui.configuration.bullModeRadioButton.toggled.connect(lambda: set_bull_mode(app, gui))
    gui.configuration.bearModeRadioButton.toggled.connect(lambda: set_bear_mode(app, gui))
    # gui.configuration.simpleLoggingRadioButton.clicked.connect(lambda: gui.set_advanced_logging(False))
    # gui.configuration.advancedLoggingRadioButton.clicked.connect(lambda: gui.set_advanced_logging(True))
    #
    # gui.configuration.updateBinanceValues.clicked.connect(gui.update_binance_values)
    # gui.configuration.updateTickers.clicked.connect(gui.tickers_thread)


def create_simulation_slots(gui):
    """
    Creates simulation slots.
    """
    gui.runButton.clicked.connect(gui.initiate_click_run_thread)
    # gui.comboBox.currentTextChanged.connect(gui.choice_table)
    gui.configureButton.clicked.connect(lambda: gui.show_simulation(gui.configuration))
    gui.pushButton_update_app.clicked.connect(gui.check_updates)

    # gui.pushButton_update_app.clicked.connect(gui.check_updates)

    gui.search_table_articul_lineEdit.textChanged.connect(gui.search_articul)
    gui.pushButton_update.clicked.connect(gui.update_table)

    gui.filter_comboBox.currentTextChanged.connect(gui.filter_data)
    # gui.pushButton_update.clicked.connect(gui.filter_data)
    gui.clearMessageTableButton.clicked.connect(lambda: clear_table(gui.activityMonitor))

    gui.endButton.clicked.connect(lambda: gui.end_bot_thread())
