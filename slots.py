"""
Slots for Algobot GUI.
"""

from caspi_pars.interface.utils import clear_table
from caspi_pars.themes import set_bear_mode, set_dark_mode, set_light_mode
from caspi_pars.interface.utils import add_to_data_table_view
from caspi_pars.db_QSqlDatabase import model_perm


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
    gui.configuration.bearModeRadioButton.toggled.connect(lambda: set_bear_mode(app, gui))


def create_simulation_slots(gui):
    """
    Creates simulation slots.
    """
    gui.comboBox_show_data_other_city.currentTextChanged.connect(lambda: add_to_data_table_view(gui, model_perm, 'permanent_table', gui.permanent_tableView))
    gui.runButton.clicked.connect(gui.initiate_click_run_thread)
    gui.configureButton.clicked.connect(lambda: gui.show_simulation(gui.configuration))
    gui.pushButton_update_app.clicked.connect(gui.check_updates)

    gui.search_table_articul_lineEdit.textChanged.connect(gui.search_articul)

    gui.pushButton_update.clicked.connect(gui.update_table)

    gui.filter_comboBox.currentTextChanged.connect(gui.filter_data)
    gui.clearMessageTableButton.clicked.connect(lambda: clear_table(gui.activityMonitor))

    gui.endButton.clicked.connect(lambda: gui.end_bot_thread())
