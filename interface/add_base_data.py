import os

from PyQt5 import uic
from sqlalchemy import MetaData

from db_tables import engine
from interface.resources_qtdesigner import add_data_to_base_rs
from helpers import resource_path
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QDataWidgetMapper, QDialog, QMainWindow, QMessageBox)
from enums import list_stores, list_cities, filter_for_goods_with_data, filter_for_goods_without_data, \
    list_stores_ini
from interface.config_utils.user_config_utils import search_line_comboBox, add_comboBox, delete_comboBox, \
    get_list_comboBox
from db_QSqlDatabase import db
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

        self.parent = parent
        # self.current_index = current_index

        self.model = QSqlTableModel(db=db)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.articul_lineEdit, 2)
        self.mapper.addMapping(self.lineEdit_2, 3)
        self.mapper.addMapping(self.current_price_lineEdit, 4)
        self.mapper.addMapping(self.first_cost_lineEdit, 5)
        self.mapper.addMapping(self.check_limiter_comboBox, 6)
        self.mapper.addMapping(self.limiter_comboBox, 7)

        self.mapper.addMapping(self.city_1_comboBox, 8)
        self.mapper.addMapping(self.min_price_lineEdit_1, 9)
        self.mapper.addMapping(self.max_price_lineEdit_1, 10)

        # (1, 2) Добавляет список в виджет, (3) Поиск выбора в виджете comboBox
        listItems = get_list_comboBox(list_stores_ini, list_stores)
        self.limiter_comboBox.addItems(listItems)
        search_line_comboBox(listItems, self.limiter_comboBox)

        # дОБАВЛЯЕТ и удаляет назв. магаза
        self.add_name_store_pushButton.clicked.connect(lambda: add_comboBox(list_stores_ini,
                                                                         self.limiter_comboBox, list_stores))
        self.remove_name_store_pushButton.clicked.connect(lambda: delete_comboBox(list_stores_ini, self.limiter_comboBox))

        # (1) Добавляет список в виджет, (2) Поиск выбора в виджете comboBox
        self.city_1_comboBox.addItems(list_cities)
        search_line_comboBox(list_cities, self.city_1_comboBox)

        # Кнопки управления
        self.previousButton.clicked.connect(self.mapper.toPrevious)
        self.nextButton.clicked.connect(self.mapper.toNext)

        # Проверяем КОРРЕкТНО Ли введеные данные
        self.saveButton.clicked.connect(self.check_condition_save)

        # Проверяет есть ли ограничитель. Если да - огр:вкл
        self.check_limiter_comboBox.currentTextChanged.connect(self.check_limiter)

        # Вычисляет мин и макс цены умножая Себест. на % соотношение
        self.min_price_spinBox_1.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.min_price_lineEdit_1, self.min_price_spinBox_1))
        self.max_price_spinBox_1.valueChanged.connect(lambda: self.calculate_min_max_price\
                                                      (self.max_price_lineEdit_1, self.max_price_spinBox_1))

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

    def filter_data(self):
        """
        Фильтрует данные на этой окошке
        """
        if self.parent.filter_comboBox.currentText() == 'Товары без данных':
            self.model.setFilter(filter_for_goods_without_data)
        elif self.parent.filter_comboBox.currentText() == 'Товары с данными':
            self.model.setFilter(filter_for_goods_with_data)
        else:
            filter_str = 'Артикул LIKE "%%"'
            self.model.setFilter(filter_str)

    def search_articul(self, s):
        filter_str = 'Артикул LIKE "%{}%"'.format(s)  # s это текст вводимый в поле поиска
        self.model.setFilter(filter_str)

    def calculate_min_max_price(self, widget_lineEdit, widget_spinBox):
        """
        """
        try:
            min_max_price = int((int(self.first_cost_lineEdit.text()) * widget_spinBox.value()) / 100 + \
                                int(self.first_cost_lineEdit.text()))
            widget_lineEdit.setText(str(min_max_price))
            # curr_articul = self.articul_lineEdit.text()
            # print('curr_articul: ', curr_articul)
            # curr_row = session.query(percent_price_table).filter(percent_price_table.c.Артикул == curr_articul).one()
            # print(curr_row)
            # conn.execute(percent_price_table.insert().values(Город_1_мин_ценаПроценты=self.min_price_spinBox_1.value(), Город_1_макс_ценаПроценты=self.max_price_spinBox_1.value()))
            # curr_row.Город_1_мин_ценаПроценты = self.min_price_spinBox_1.value()
            # session.commit()
            # # curr_row.Город_1_макс_ценаПроценты =
        except Exception:
            print('calculate_min_max_price:', Exception)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setText('Нужно записать целочисленное значение в Себестоимость!')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def check_limiter(self):
        if self.check_limiter_comboBox.currentText() == 'Нет':
            self.limiter_comboBox.setEnabled(False)
            self.add_name_store_pushButton.setEnabled(False)
            self.remove_name_store_pushButton.setEnabled(False)

        else:
            self.limiter_comboBox.setEnabled(True)
            self.add_name_store_pushButton.setEnabled(True)
            self.remove_name_store_pushButton.setEnabled(True)

    def check_condition_save(self):
        """
        Проверка условии на - правильно ли
        введены данные
        """
        try:
            if not (int(self.current_price_lineEdit.text())/3 < int(self.first_cost_lineEdit.text()) < int(self.current_price_lineEdit.text())*3):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка")
                msg.setText('Значение себестоимости слишком занижена \nили завышена от текущей цены')
                msg.setWindowTitle("Ошибка")
                msg.exec_()

            elif self.city_1_comboBox.currentText() not in list_cities:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка")
                msg.setText('Выберите город из списка(Город №)')
                msg.setWindowTitle("Ошибка")
                msg.exec_()

            else:
                self.mapper.submit()
                self.parent.filter_data()

        except Exception as ex:
            print('check_condition_save: ', ex)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setText('Нужно записать целочисленное \nзначение в Себестоимость!')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    # def insert_percent_price_to_table(self):
    #     curr_articul = self.articul_lineEdit.text()
    #     print('curr_articul: ', curr_articul)
    #     curr_row = session.query(percent_price_table).filter(percent_price_table.c.Артикул == curr_articul).one()
    #     curr_row.Город_1_мин_ценаПроценты = self.min_price_spinBox_1.value()
    #     curr_row.Город_1_макс_ценаПроценты = self.max_price_spinBox_1.value()

