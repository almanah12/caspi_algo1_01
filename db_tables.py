import os

from sqlalchemy import create_engine, select, Table, Column, Integer, MetaData, ForeignKey, TEXT, Float
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from caspi_pars.helpers import resource_path

meta = MetaData()
# Временная таблица куда сохраним данные товаров магаза
temporary_table = Table('temporary_table', meta,
                        Column('Артикул', Integer),
                        Column('Модель', TEXT),
                        Column('Брэнд', TEXT),
                        Column('Ссылка', TEXT),
                        Column('Текущая_ц', Integer),
                        Column('Доступность', TEXT),
                        Column('Колич_городов', Integer),
                        Column('Город_1', TEXT),
                        Column('Г_1_Конк', TEXT),
                        Column('Г_1_новая_ц', Integer),
                        Column('Город_2', TEXT),
                        Column('Г_2_Конк', TEXT),
                        Column('Г_2_новая_ц', Integer),
                        Column('Город_3', TEXT),
                        Column('Г_3_Конк', TEXT),
                        Column('Г_3_новая_ц', Integer),
                        Column('Город_4', TEXT),
                        Column('Г_4_Конк', TEXT),
                        Column('Г_4_новая_ц', Integer)
                        )

# Постояная таблица куда сохраним данные товаров магаза
permanent_table = Table('permanent_table', meta,
                        Column('E', Integer),
                        Column('D', Integer),
                        Column('Артикул', Integer),
                        Column('Модель', TEXT),
                        Column('Город_1', TEXT),
                        Column('Тек_п1', Integer),
                        Column('Текущая_ц', Integer),  # 5
                        Column('Себестоимость', Integer),
                        Column('Есть_огрч', TEXT),
                        Column('Ограничитель', TEXT),
                        Column('Г_1_мин_ц_проц', Float),  # 10
                        Column('Г_1_мин_ц', Integer),
                        Column('Г_1_макс_ц_проц', Float),
                        Column('Г_1_макс_ц', Integer),
                        Column('Город_2', TEXT),
                        Column('Тек_п1', Integer),
                        Column('Текущая_ц', Integer),
                        Column('Себестоимость', Integer),  # 5
                        Column('Г_2_мин_ц', Integer),  # 15
                        Column('Г_2_макс_ц', Integer),
                        Column('Город_3', TEXT),
                        Column('Г_3_мин_ц', Integer),
                        Column('Г_3_макс_ц', Integer),
                        Column('Город_4', TEXT),  # 20
                        Column('Г_4_мин_ц', Integer),
                        Column('Г_4_макс_ц', Integer),
                        )

if not os.path.exists(resource_path('data_shop')):
    os.mkdir(resource_path('data_shop'))

res_path = resource_path(r'data_shop/dt_goods.sqlite')
engine = create_engine(r"sqlite:///"+res_path, connect_args={'check_same_thread': False}, poolclass=StaticPool, echo=False)

meta.create_all(engine)  # или books.create(engine), authors.create(engine)
conn_engine = engine.connect()
temp_table_select = select(temporary_table)
perm_table_select = select(permanent_table)
Session = sessionmaker(bind=engine)
session = Session()
