"""
Slots helper functions for configuration.py can be found here.
"""
from PyQt5.QtWidgets import QFileDialog
from caspi_pars.interface.config_utils.user_config_utils import list_proxy_folder, delete_comboBox, add_comboBox, \
    list_proxy_folder1, add_pp, clear_pp, add_city
from caspi_pars.enums import list_stores, list_stores_ini
from caspi_pars.helpers import resource_path

def load_slots(config_obj):
    """
    Loads all configuration interface slots.
    :param config_obj: Configuration QDialog object (from configuration.py)
    :return: None
    """
    config = config_obj
    config.load_list_proxy_pushButton.clicked.connect(lambda: list_proxy_folder(gui=config, typeFile='text files(*.txt)',
                                                                           widget=config.list_proxy_path_lineEdit))
    # config.path_for_saveXML_pushButton.clicked.connect(lambda: list_proxy_folder1(gui=config, typeFile='xml files(*.xml)',
    #                                                                         widget=config.path_save_xml_lineEdit))
    config.list_articulpushButton.clicked.connect(lambda: QFileDialog.getOpenFileName())

    # дОБАВЛЯЕТ и удаляет назв. магаза
    config.add_name_store_pushButton.clicked.connect(lambda: add_comboBox(list_stores_ini,
                                                                        config.name_store_comboBox, list_stores))
    config.remove_name_store_pushButton.clicked.connect(lambda: delete_comboBox(list_stores_ini, config.name_store_comboBox))

    # дОБАВЛЯЕТ и удаляет назв. точки продаж
    config.pushButton_add_pp.clicked.connect(lambda: add_pp(config))
    config.pushButton_clear_all_pp.clicked.connect(lambda: clear_pp(config))
    config.pushButton_add_city.clicked.connect(lambda: add_city(config))




