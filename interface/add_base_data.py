import loguru
from PyQt5 import uic

from caspi_pars.interface.resources_qtdesigner import add_data_to_base_rs
from caspi_pars.helpers import resource_path
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QDataWidgetMapper, QDialog, QMainWindow)
from caspi_pars.interface.config_utils.user_config_utils import search_line_comboBox, add_comboBox, delete_comboBox, \
    get_list_comboBox
from caspi_pars.db_QSqlDatabase import db, model_perm
from caspi_pars.db_tables import session, permanent_table, temporary_table
from caspi_pars.enums import filter_for_goods_with_data, filter_for_goods_without_data, list_stores, list_stores_ini, \
    filter_all_active_data, filter_all_data
from caspi_pars.other_func.check_data_fill import ch_data_fill

#
# if not os.path.exists(resource_path('data_shop')):
#     os.mkdir(resource_path('data_shop'))

# meta = MetaData()
# meta.create_all(engine)
# db = QSqlDatabase("QSQLITE")
# db.setDatabaseName(resource_path(r"data_shop/dt_goods.sqlite"))
# db.open()


class Add_Base_Data(QDialog):
    def __init__(self, parent: QMainWindow):

        add_data_to_base_rs.qInitResources()
        super(Add_Base_Data, self).__init__(parent)  # Initializing object
        uic.loadUi(resource_path(r'UI/add_data_to_base.ui'), self)  # Loading the main UI

        self.add_b_d_dict = {
                'current_price_1': self.current_price_lineEdit_1,
                'first_cost_1': self.first_cost_lineEdit_1,
                'min_price_1': self.min_price_lineEdit_1,
                'max_price_1': self.max_price_lineEdit_1,
                'min_price_spinBox_1': self.min_price_spinBox_1,
                'max_price_spinBox_1': self.max_price_spinBox_1,

                'current_price_2': self.current_price_lineEdit_2,
                'first_cost_2': self.first_cost_lineEdit_2,
                'min_price_2': self.min_price_lineEdit_2,
                'max_price_2': self.max_price_lineEdit_2,
                'min_price_spinBox_2': self.min_price_spinBox_2,
                'max_price_spinBox_2': self.max_price_spinBox_2,

                'current_price_3': self.current_price_lineEdit_3,
                'first_cost_3': self.first_cost_lineEdit_3,
                'min_price_3': self.min_price_lineEdit_3,
                'max_price_3': self.max_price_lineEdit_3,
                'min_price_spinBox_3': self.min_price_spinBox_3,
                'max_price_spinBox_3': self.max_price_spinBox_3,

                'current_price_4': self.current_price_lineEdit_4,
                'first_cost_4': self.first_cost_lineEdit_4,
                'min_price_4': self.min_price_lineEdit_4,
                'max_price_4': self.max_price_lineEdit_4,
                'min_price_spinBox_4': self.min_price_spinBox_4,
                'max_price_spinBox_4': self.max_price_spinBox_4,
            }

        self.parent = parent
        # self.current_index = current_index

        self.model = QSqlTableModel(db=db)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.articul_lineEdit, 2)
        self.mapper.addMapping(self.lineEdit_2, 3)
        self.mapper.addMapping(self.check_limiter_comboBox, 4)
        self.mapper.addMapping(self.limiter_comboBox, 5)

        self.mapper.addMapping(self.current_price_lineEdit_1, 8)
        self.mapper.addMapping(self.first_cost_lineEdit_1, 9)
        self.mapper.addMapping(self.min_price_spinBox_1, 10)
        self.mapper.addMapping(self.min_price_lineEdit_1, 11)
        self.mapper.addMapping(self.max_price_spinBox_1, 12)
        self.mapper.addMapping(self.max_price_lineEdit_1, 13)

        self.mapper.addMapping(self.current_price_lineEdit_2, 16)
        self.mapper.addMapping(self.first_cost_lineEdit_2, 17)
        self.mapper.addMapping(self.min_price_spinBox_2, 18)
        self.mapper.addMapping(self.min_price_lineEdit_2, 19)
        self.mapper.addMapping(self.max_price_spinBox_2, 20)
        self.mapper.addMapping(self.max_price_lineEdit_2, 21)

        self.mapper.addMapping(self.current_price_lineEdit_3, 24)
        self.mapper.addMapping(self.first_cost_lineEdit_3, 25)
        self.mapper.addMapping(self.min_price_spinBox_3, 26)
        self.mapper.addMapping(self.min_price_lineEdit_3, 27)
        self.mapper.addMapping(self.max_price_spinBox_3, 28)
        self.mapper.addMapping(self.max_price_lineEdit_3, 29)

        self.mapper.addMapping(self.current_price_lineEdit_4, 32)
        self.mapper.addMapping(self.first_cost_lineEdit_4, 33)
        self.mapper.addMapping(self.min_price_spinBox_4, 34)
        self.mapper.addMapping(self.min_price_lineEdit_4, 35)
        self.mapper.addMapping(self.max_price_spinBox_4, 36)
        self.mapper.addMapping(self.max_price_lineEdit_4, 37)

        # (1, 2) Добавляет список в виджет, (3) Поиск выбора в виджете comboBox
        listItems = get_list_comboBox(list_stores_ini, list_stores)
        self.limiter_comboBox.addItems(listItems)
        search_line_comboBox(listItems, self.limiter_comboBox)

        # дОБАВЛЯЕТ и удаляет назв. магаза
        self.add_name_store_pushButton.clicked.connect(lambda: add_comboBox(list_stores_ini,
                                                                         self.limiter_comboBox, list_stores))
        self.remove_name_store_pushButton.clicked.connect(lambda: delete_comboBox(list_stores_ini, self.limiter_comboBox))

        # # (1) Добавляет список в виджет, (2) Поиск выбора в виджете comboBox
        # self.city_1_comboBox.addItems(list_cities)
        # search_line_comboBox(list_cities, self.city_1_comboBox)
        # Проверяем КОРРЕкТНО Ли введеные данные
        self.saveButton.clicked.connect(self.check_full_data_bool)

        # Кнопки управления
        self.previousButton.clicked.connect(self.previous_button)
        self.nextButton.clicked.connect(self.next_button)



        # Проверяет есть ли ограничитель. Если да - огр:вкл
        self.check_limiter_comboBox.currentTextChanged.connect(self.check_limiter)

        # Проверяет
        self.check_limiter_comboBox.currentTextChanged.connect(self.check_limiter)

        # Вычисляет мин и макс цены умножая Себест. на % соотношение
        # Город_1
        self.min_price_spinBox_1.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_1, self.min_price_lineEdit_1, self.min_price_spinBox_1))
        self.max_price_spinBox_1.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_1,self.max_price_lineEdit_1, self.max_price_spinBox_1))
        self.first_cost_lineEdit_1.textChanged.connect(lambda: self.calculate_min_max_price \
                                                    (self.first_cost_lineEdit_1, self.min_price_lineEdit_1, self.min_price_spinBox_1))
        self.first_cost_lineEdit_1.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_1, self.max_price_lineEdit_1, self.max_price_spinBox_1))

        # Город_2
        self.min_price_spinBox_2.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_2, self.min_price_lineEdit_2, self.min_price_spinBox_2))
        self.max_price_spinBox_2.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_2, self.max_price_lineEdit_2, self.max_price_spinBox_2))
        self.first_cost_lineEdit_2.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_2, self.min_price_lineEdit_2, self.min_price_spinBox_2))
        self.first_cost_lineEdit_2.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_2, self.max_price_lineEdit_2, self.max_price_spinBox_2))
        # Город_3
        self.min_price_spinBox_3.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_3, self.min_price_lineEdit_3, self.min_price_spinBox_3))
        self.max_price_spinBox_3.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_3, self.max_price_lineEdit_3, self.max_price_spinBox_3))
        self.first_cost_lineEdit_3.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_3, self.min_price_lineEdit_3, self.min_price_spinBox_3))
        self.first_cost_lineEdit_3.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_3, self.max_price_lineEdit_3, self.max_price_spinBox_3))


        # Город_4
        self.min_price_spinBox_4.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_4, self.min_price_lineEdit_4, self.min_price_spinBox_4))
        self.max_price_spinBox_4.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_4, self.max_price_lineEdit_4, self.max_price_spinBox_4))
        self.first_cost_lineEdit_4.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_4, self.min_price_lineEdit_4, self.min_price_spinBox_4))
        self.first_cost_lineEdit_4.textChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.first_cost_lineEdit_4, self.max_price_lineEdit_4, self.max_price_spinBox_4))
        # self.tabWidget.itemClicked.connect(self.city_visible)

        # Ставит в модель таблицу
        self.model.setTable("permanent_table")

        # Упорядочивает данные по фильтру
        self.filter_data()

        self.search_articul(self.parent.search_table_articul_lineEdit.text())

        # Заполняет модель данными
        self.model.select()

    def init_delegate(self, current_index):
        # Выводить данные с текущим индексом
        self.mapper.setCurrentIndex(current_index)
        self.tab_widget_manipulation()

    def next_button(self):
        self.mapper.toNext()
        self.tab_widget_manipulation()

    def previous_button(self):
        self.mapper.toPrevious()
        self.tab_widget_manipulation()

    def tab_widget_manipulation(self):
        curr_row = session.query(permanent_table). \
            filter(permanent_table.c.Артикул == self.articul_lineEdit.text()).first()
        for i in range(self.tabWidget.count()):
            self.tabWidget.setTabEnabled(i, True)
            if not curr_row['Город_{}'.format(i+1)]:
                self.tabWidget.setTabEnabled(i, False)
                self.tabWidget.setTabText(i, 'Город {}'.format(i + 1))
            else:
                self.tabWidget.setTabText(i, curr_row['Город_{}'.format(i + 1)])

    def filter_data(self):
        """
        Фильтрует данные на этой окошке
        """
        if self.parent.filter_comboBox.currentText() == 'Товары без данных':
            self.model.setFilter(filter_for_goods_without_data)
        elif self.parent.filter_comboBox.currentText() == 'Товары с данными':
            self.model.setFilter(filter_for_goods_with_data)
        elif self.parent.filter_comboBox.currentText() == 'Активные':
            self.model.setFilter(filter_all_active_data)
        else:
            model_perm.setFilter(filter_all_data)

    def search_articul(self, s):
        filter_str = 'Артикул LIKE "%{}%"'.format(s)  # s это текст вводимый в поле поиска
        self.model.setFilter(filter_str)

    def calculate_min_max_price(self, first_cost, widget_lineEdit, widget_spinBox):
        """
        """
        if first_cost.text():
            min_max_price = int((int(first_cost.text()) * widget_spinBox.value())/100 + \
                                int(first_cost.text()))
            widget_lineEdit.setText(str(min_max_price))
        else:
            widget_lineEdit.clear()

        # except Exception as ex:
        #     msg = QMessageBox()
        #     loguru.logger.debug(ex)
        #     msg.setIcon(QMessageBox.Critical)
        #     msg.setText("Ошибка")
        #     msg.setText('Нужно записать целочисленное значение в Себестоимость!')
        #     msg.setWindowTitle("Ошибка")
        #     msg.exec_()

    def check_limiter(self):
        if self.check_limiter_comboBox.currentText() == 'Нет':
            self.limiter_comboBox.setEnabled(False)
            self.add_name_store_pushButton.setEnabled(False)
            self.remove_name_store_pushButton.setEnabled(False)

        else:
            self.limiter_comboBox.setEnabled(True)
            self.add_name_store_pushButton.setEnabled(True)
            self.remove_name_store_pushButton.setEnabled(True)

    def check_full_data_bool(self):
        # full_data_bool = ch_data_fill(self.parent)
        # if full_data_bool[0]:
        self.mapper.submit()
        self.parent.update_table()

        #     else:
    #         msg = QMessageBox()
    #         msg.setIcon(QMessageBox.Critical)
    #         msg.setText("Условие: Разные цены для городов")
    #         msg.setText('Заполните данные всех городов')
    #         msg.setWindowTitle("Ошибка")
    #         msg.exec_()
        # if not (int(self.current_price_lineEdit.text())/3 < int(self.first_cost_lineEdit.text()) < int(self.current_price_lineEdit.text())*3):
        #     msg = QMessageBox()
        #     msg.setIcon(QMessageBox.Critical)
        #     msg.setText("Ошибка")
        #     msg.setText('Значение себестоимости слишком занижена \nили завышена от текущей цены')
        #     msg.setWindowTitle("Ошибка")
        #     msg.exec_()




