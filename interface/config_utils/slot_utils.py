"""
Slots helper functions for configuration.py can be found here.
"""
from PyQt5.QtWidgets import (QCheckBox, QDoubleSpinBox, QHBoxLayout, QLabel, QScrollArea, QSpinBox, QTabWidget,
                             QVBoxLayout)

from interface.config_utils.user_config_utils import list_proxy_folder, delete_comboBox, add_comboBox, \
    list_proxy_folder1
from enums import list_stores, list_stores_ini


def load_slots(config_obj):
    """
    Loads all configuration interface slots.
    :param config_obj: Configuration QDialog object (from configuration.py)
    :return: None
    """
    c = config_obj
    c.load_list_proxy_pushButton.clicked.connect(lambda: list_proxy_folder(gui=c, typeFile='text files(*.txt)',
                                                                           widget=c.list_proxy_path_lineEdit))
    c.path_for_saveXML_pushButton.clicked.connect(lambda: list_proxy_folder1(gui=c, typeFile='xml files(*.xml)',
                                                                            widget=c.path_save_xml_lineEdit))
    c.list_articulpushButton.clicked.connect(lambda: list_proxy_folder(gui=c, typeFile='csv files(*.csv)',
                                                                            widget=c.list_articullineEdit))

    # дОБАВЛЯЕТ и удаляет назв. магаза
    c.add_name_store_pushButton.clicked.connect(lambda: add_comboBox(list_stores_ini,
                                                                        c.name_store_comboBox, list_stores))
    c.remove_name_store_pushButton.clicked.connect(lambda: delete_comboBox(list_stores_ini, c.name_store_comboBox))


