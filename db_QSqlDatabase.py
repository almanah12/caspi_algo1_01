from PyQt5 import QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel
from caspi_pars.helpers import resource_path

db = QSqlDatabase("QSQLITE")
db.setDatabaseName(resource_path(r"data_shop/dt_goods.sqlite"))
db.open()


model_perm = QSqlTableModel(db=db)
model_perm.setTable("permanent_table") # указываем таблицу из БД для модели
model_perm.select()

model_temp = QSqlTableModel(db=db)
model_temp.setTable("temporary_table")  # указываем таблицу из БД для модели
model_temp.select()