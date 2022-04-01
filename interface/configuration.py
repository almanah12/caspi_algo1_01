"""
Configuration window.
"""
from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (QDialog, QMainWindow)

from caspi_pars.interface.resources_qtdesigner import conf_rs
from caspi_pars.enums import list_stores_ini, list_stores, list_cities, list_PP, list_number_cities
from caspi_pars.helpers import resource_path
from caspi_pars.interface.config_utils.slot_utils import load_slots
from caspi_pars.interface.config_utils.user_config_utils import search_line_comboBox, save_comboBox, get_list_comboBox


class Configuration(QDialog):
    """
    Configuration window.
    """
    def __init__(self, parent: QMainWindow):
        conf_rs.qInitResources()
        super(Configuration, self).__init__(parent)  # Initializing object
        self.CONFIG_FILE_NAME = resource_path(r'data_shop/config.ini')

        uic.loadUi(resource_path(r'UI/configuration.ui'), self)  # Loading the main UI
        self.parent = parent
        # self.threadPool = QThreadPool()
        # self.setting_window = QSettings('AlashParsConf', 'Window size')
        # self.setting_variables = QSettings('AlashParsConf', 'Variables')
        self.setting_variables = QSettings(self.CONFIG_FILE_NAME, QSettings.IniFormat)

        # (1, 2) Добавляет список в виджет, (3) Поиск выбора в виджете comboBox
        listItems = get_list_comboBox(list_stores_ini, list_stores)
        self.name_store_comboBox.addItems(listItems)
        search_line_comboBox(listItems, self.name_store_comboBox)

        # Добавляет список городов в виджеты comboBox
        self.set_list_cities_comboBoxes()

        # Делаеет виджеты невидимыми
        self.visible_useProxy()
        self.use_proxy_comboBox.currentTextChanged.connect(self.visible_useProxy)

        self.visible_list_articul()
        self.list_articulcomboBox.currentTextChanged.connect(self.visible_list_articul)

        self.visible_google_cloud()
        self.auto_downl_xml_to_google_comboBox.currentTextChanged.connect(self.visible_google_cloud)

        load_slots(self)

        #
        self.set_widgets_values()

    def set_widgets_values(self):
        # нАСТРОЙКИ ПАРСИНГА

        self.password_lineEdit.setText(self.setting_variables.value('password'))
        self.email_login_lineEdit.setText(self.setting_variables.value('email'))
        self.name_store_comboBox.setCurrentText(self.setting_variables.value('name_store'))
        self.id_partner_lineEdit.setText(self.setting_variables.value('id_partner'))
        self.interval_from_spinBox.setValue(self.setting_variables.value('interval_from', type=int))
        self.interval_before_spinBox.setValue(self.setting_variables.value('interval_before', type=int))
        self.number_thread_spinBox.setValue(self.setting_variables.value('number_thread', type=int))
        self.use_proxy_comboBox.setCurrentText(self.setting_variables.value('use_proxy'))
        self.list_proxy_path_lineEdit.setText(self.setting_variables.value('list_proxy_path'))
        self.type_proxy_comboBox.setCurrentText(self.setting_variables.value('type_proxy'))

        # Точки доступа
        self.lineEdit_city_name_1.setText(self.setting_variables.value('city_name_1'))
        self.lineEdit_seller_points_1.setText(self.setting_variables.value('seller_points_1'))
        self.lineEdit_city_name_2.setText(self.setting_variables.value('city_name_2'))
        self.lineEdit_seller_points_2.setText(self.setting_variables.value('seller_points_2'))
        self.lineEdit_city_name_3.setText(self.setting_variables.value('city_name_3'))
        self.lineEdit_seller_points_3.setText(self.setting_variables.value('seller_points_3'))
        self.lineEdit_city_name_4.setText(self.setting_variables.value('city_name_4'))
        self.lineEdit_seller_points_4.setText(self.setting_variables.value('seller_points_4'))


        # Наценка
        self.same_price_citiesradioButton.setChecked(self.setting_variables.value('same_price_cities', type=bool))
        self.different_price_citiesradioButton.setChecked(self.setting_variables.value('different_price_cities', type=bool))
        # self.same_price_cities_checkBox.setCheckState(
        #     self.setting_variables.value('same_price_cities', QtCore.Qt.Checked, QtCore.Qt.CheckState))
        # self.different_price_cities_checkBox.setCheckState(
        #     self.setting_variables.value('different_price_cities', QtCore.Qt.Checked, QtCore.Qt.CheckState))
        self.interval_change_price_spinBox.setValue(self.setting_variables.value('interval_change_price', type=int))
        self.consider_deliver_times_comboBox.setCurrentText(self.setting_variables.value('deliver_times'))
        self.use_base_limit_comboBox.setCurrentText(self.setting_variables.value('use_base_limit'))
        self.up_price_to_competitor_comboBox.setCurrentText(self.setting_variables.value('up_price_to_competitor'))
        self.list_articulcomboBox.setCurrentText(self.setting_variables.value('list_articul'))
        self.list_articullineEdit.setText(self.setting_variables.value('path_list_articul'))

        # Файл
        # self.path_save_xml_lineEdit.setText(self.setting_variables.value('path_save_xml'))
        self.auto_downl_xml_comboBox.setCurrentText(self.setting_variables.value('auto_downl_xml'))
        self.auto_downl_xml_to_google_comboBox.setCurrentText(self.setting_variables.value('auto_downl_xml_to_google_comboBox'))
        self.name_xml_file_lineEdit.setText(self.setting_variables.value('name_xml_file'))
        self.name_folder_lineEdit.setText(self.setting_variables.value('name_folder'))

        # Настройки приложения
        self.lightModeRadioButton.setChecked(self.setting_variables.value('lightMode', type=bool))
        self.darkModeRadioButton.setChecked(self.setting_variables.value('darkMode', type=bool))
        self.bearModeRadioButton.setChecked(self.setting_variables.value('bearMode', type=bool))

    def closeEvent(self, event):

        save_comboBox(list_stores_ini, self.name_store_comboBox)
        # нАСТРОЙКИ ПАРСИНГА
        self.setting_variables.setValue('password', self.password_lineEdit.text())
        self.setting_variables.setValue('email', self.email_login_lineEdit.text())
        self.setting_variables.setValue('name_store', self.name_store_comboBox.currentText())
        self.setting_variables.setValue('id_partner', self.id_partner_lineEdit.text())
        self.setting_variables.setValue('interval_from', self.interval_from_spinBox.value())
        self.setting_variables.setValue('interval_before', self.interval_before_spinBox.value())
        self.setting_variables.setValue('number_thread', self.number_thread_spinBox.value())
        self.setting_variables.setValue('use_proxy', self.use_proxy_comboBox.currentText())
        self.setting_variables.setValue('list_proxy_path', self.list_proxy_path_lineEdit.text())
        self.setting_variables.setValue('type_proxy', self.type_proxy_comboBox.currentText())

        # Точки доступа
        self.setting_variables.setValue('city_name_1', self.lineEdit_city_name_1.text())
        self.setting_variables.setValue('seller_points_1', self.lineEdit_seller_points_1.text())
        self.setting_variables.setValue('city_name_2', self.lineEdit_city_name_2.text())
        self.setting_variables.setValue('seller_points_2', self.lineEdit_seller_points_2.text())
        self.setting_variables.setValue('city_name_3', self.lineEdit_city_name_3.text())
        self.setting_variables.setValue('seller_points_3', self.lineEdit_seller_points_3.text())
        self.setting_variables.setValue('city_name_4', self.lineEdit_city_name_4.text())
        self.setting_variables.setValue('seller_points_4', self.lineEdit_seller_points_4.text())

        # Наценка
        self.setting_variables.setValue('same_price_cities', self.same_price_citiesradioButton.isChecked())
        self.setting_variables.setValue('different_price_cities', self.different_price_citiesradioButton.isChecked())
        self.setting_variables.setValue('interval_change_price', self.interval_change_price_spinBox.value())
        self.setting_variables.setValue('use_base_limit', self.use_base_limit_comboBox.currentText())
        self.setting_variables.setValue('deliver_times', self.consider_deliver_times_comboBox.currentText())
        self.setting_variables.setValue('up_price_to_competitor', self.up_price_to_competitor_comboBox.currentText())
        self.setting_variables.setValue('list_articul', self.list_articulcomboBox.currentText())
        self.setting_variables.setValue('path_list_articul', self.list_articullineEdit.text())

        # Файл
        # self.setting_variables.setValue('path_save_xml', self.path_save_xml_lineEdit.text())
        self.setting_variables.setValue('auto_downl_xml', self.auto_downl_xml_comboBox.currentText())
        self.setting_variables.setValue('auto_downl_xml_to_google_comboBox', self.auto_downl_xml_to_google_comboBox.currentText())
        self.setting_variables.setValue('name_xml_file', self.name_xml_file_lineEdit.text())
        self.setting_variables.setValue('name_folder', self.name_folder_lineEdit.text())

        # Настройки приложения
        self.setting_variables.setValue('lightMode', self.lightModeRadioButton.isChecked())
        self.setting_variables.setValue('darkMode', self.darkModeRadioButton.isChecked())
        self.setting_variables.setValue('bearMode', self.bearModeRadioButton.isChecked())

    def visible_useProxy(self):
        if self.use_proxy_comboBox.currentText() == 'Нет':
            self.list_proxy_path_lineEdit.setVisible(False)
            self.load_list_proxy_pushButton.setVisible(False)
            self.type_proxy_comboBox.setVisible(False)

            self.label_22.setVisible(False)
            self.label_23.setVisible(False)

        else:
            self.list_proxy_path_lineEdit.setVisible(True)
            self.load_list_proxy_pushButton.setVisible(True)
            self.type_proxy_comboBox.setVisible(True)

            self.label_22.setVisible(True)
            self.label_23.setVisible(True)

    def visible_list_articul(self):
        if self.list_articulcomboBox.currentText() == 'Нет':
            self.list_articulpushButton.setVisible(False)
            self.list_articullineEdit.setVisible(False)
            self.label_24.setVisible(False)

        else:
            self.list_articulpushButton.setVisible(True)
            self.list_articullineEdit.setVisible(True)

            self.label_24.setVisible(True)

    def visible_google_cloud(self):
        if self.auto_downl_xml_to_google_comboBox.currentText() == 'Нет':
            self.label_25.setVisible(False)
            self.label_26.setVisible(False)
            self.name_xml_file_lineEdit.setVisible(False)
            self.name_folder_lineEdit.setVisible(False)

        else:
            self.label_25.setVisible(True)
            self.label_26.setVisible(True)
            self.name_xml_file_lineEdit.setVisible(True)
            self.name_folder_lineEdit.setVisible(True)

    def set_list_cities_comboBoxes(self):
        # (1) Добавляет список в виджет, (2) Поиск выбора в виджете comboBox
        self.comboBox_name_city.addItems(list_cities)
        # search_line_comboBox(list_cities, self.comboBox_name_city_1)
        self.comboBox_list_name_pp.addItems(list_PP)
        self.comboBox_number_cities.addItems(list_number_cities)

    def condition_filled_data_in_settings(self):
        value_bool = bool(self.email_login_lineEdit.text())*bool(self.password_lineEdit.text()) *\
                     bool(self.name_store_comboBox.currentText())*bool(self.id_partner_lineEdit.text()) *\
                     bool(self.name_xml_file_lineEdit.text())*bool(self.lineEdit_city_name_1.text())*\
                     bool(self.lineEdit_seller_points_1.text())
        return value_bool

        # if self.name_xml_file_lineEdit.text() is None or self.name_xml_file_lineEdit.text() == '':
        #     self.auto_downl_xml_comboBox.setCurrentText('Нет')
        #     QMessageBox.critical(self, 'Ошибка', 'Нужно заполнить поле "Название xml файла в сервере"')

        # else:
        #     self.worker_boss = auto_loading_xml_thread.RunThread(gui=self)
        #     self.threadPool.start(self.worker_boss)
