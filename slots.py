"""
Slots for Algobot GUI.
"""

from caspi_pars.interface.utils import clear_table, add_to_data_table_view
from caspi_pars.db_QSqlDatabase import model_perm
from caspi_pars.threads.runThreadMethods.kaspi_merchant import MerchantInfo

def initiate_slots(app, gui):
    """
    Initiates all interface slots.
    """
    create_interface_slots(gui)


def create_interface_slots(gui):
    """
    Creates interface slots.
    """
    create_simulation_slots(gui)


def create_simulation_slots(gui):
    """
    Creates simulation slots.
    """
    gui.runButton.clicked.connect(gui.initiate_click_run_thread)
    gui.configureButton.clicked.connect(lambda: gui.show_simulation(gui.configuration))
    gui.clearMessageTableButton.clicked.connect(lambda: clear_table(gui.activityMonitor))
    gui.endButton.clicked.connect(lambda: gui.end_bot_thread())

    gui.comboBox_show_data_other_city.currentTextChanged.connect(lambda: add_to_data_table_view(gui, model_perm, 'permanent_table', gui.permanent_tableView))
    gui.pushButton_update.clicked.connect(gui.update_table)
    gui.comboBox_search_name.currentTextChanged.connect(gui.search_table_articul_lineEdit.clear)
    gui.search_table_articul_lineEdit.textChanged.connect(gui.filter_data)
    gui.filter_comboBox.currentTextChanged.connect(lambda: gui.checkbox(0))
    gui.filter_comboBox.currentTextChanged.connect(lambda: gui.filter_data(gui.search_table_articul_lineEdit.text()))
    gui.filter_comboBox.currentTextChanged.connect(lambda: add_to_data_table_view(gui, model_perm, 'permanent_table', gui.permanent_tableView))
    gui.checkBox_tableview.stateChanged.connect(gui.check_box_table)

    gui.pushButton_downlodad_installment.clicked.connect(lambda: MerchantInfo(gui=gui).merchant_info)
    gui.comboBox_auto_confirm_order.currentTextChanged.connect(lambda: gui.thread_func(gui.auto_confirm_order_cond))
    gui.pushButton_update_app.clicked.connect(gui.check_updates)

    gui.comboBox_fill_data_table.activated.connect(lambda: visible_fill_data_parametrs(gui))
    gui.pushButton_hide_fill_data_t.clicked.connect(lambda: hide_fill_data_sets(gui))
    gui.pushButton_execute_fill_data_t.clicked.connect(lambda: gui.thread_func(gui.fill_data))


def init_other_comm(gui):
    gui.comboBox_show_data_other_city.setToolTip("Показывает данные для определеннго числа городов")
    gui.filter_comboBox.setToolTip("Фильтр данных")
    gui.pushButton_path_to_excel_1c.setToolTip("Путь к файлу Excel(1С) для обн. данных")
    gui.pushButton_update.setToolTip("Обновить данные")

    gui.checkBox_tableview.setStyleSheet("QCheckBox::indicator"
                                          "{"
                                          "width :22px;"
                                          "height : 22px;"
                                          "}")
    gui.checkBox_tableview.setToolTip("Выделить данные")
    hide_fill_data_sets(gui)


def hide_fill_data_sets(gui):
    # Заполнить данные
    gui.label_2.setVisible(False)
    gui.label_3.setVisible(False)
    gui.label_6.setVisible(False)
    gui.label_4.setVisible(False)

    gui.doubleSpinBox_first_price_caf.setVisible(False)
    gui.doubleSpinBox_min_price_caf.setVisible(False)
    gui.doubleSpinBox_max_price_caf.setVisible(False)

    # Изменить цены
    gui.label_7.setVisible(False)
    gui.label_5.setVisible(False)

    gui.doubleSpinBox_change_price_caf.setVisible(False)
    gui.checkBox_curr_price.setVisible(False)
    gui.checkBox_first_price.setVisible(False)
    gui.checkBox_min_price.setVisible(False)
    gui.checkBox_max_price.setVisible(False)

    gui.pushButton_hide_fill_data_t.setVisible(False)
    gui.pushButton_execute_fill_data_t.setVisible(False)


def visible_fill_data_parametrs(gui):
    hide_fill_data_sets(gui)
    if gui.comboBox_fill_data_table.currentText() == 'Заполнить данные':
        gui.label_2.setVisible(True)
        gui.label_3.setVisible(True)
        gui.label_6.setVisible(True)
        gui.label_4.setVisible(True)

        gui.doubleSpinBox_first_price_caf.setVisible(True)
        gui.doubleSpinBox_min_price_caf.setVisible(True)
        gui.doubleSpinBox_max_price_caf.setVisible(True)

        gui.pushButton_hide_fill_data_t.setVisible(True)
        gui.pushButton_execute_fill_data_t.setVisible(True)

    else:
        gui.label_7.setVisible(True)
        gui.label_5.setVisible(True)

        gui.doubleSpinBox_change_price_caf.setVisible(True)
        gui.checkBox_curr_price.setVisible(True)
        gui.checkBox_first_price.setVisible(True)

        gui.checkBox_min_price.setVisible(True)
        gui.checkBox_max_price.setVisible(True)
        gui.pushButton_hide_fill_data_t.setVisible(True)
        gui.pushButton_execute_fill_data_t.setVisible(True)

