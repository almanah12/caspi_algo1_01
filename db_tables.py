import os

from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, TEXT
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from helpers import resource_path

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
                        Column('Город_1_Конк', TEXT),
                        Column('Город_1_новая_ц', Integer),
                        Column('Город_2', TEXT),
                        Column('Город_2_Конк', TEXT),
                        Column('Город_2_новая_ц', Integer),
                        Column('Город_3', TEXT),
                        Column('Город_3_Конк', TEXT),
                        Column('Город_3_новая_ц', Integer),
                        Column('Город_4', TEXT),
                        Column('Город_4_Конк', TEXT),
                        Column('Город_4_новая_ц', Integer)
                        )

# Постояная таблица куда сохраним данные товаров магаза
permanent_table = Table('permanent_table', meta,
                        Column('E', Integer),
                        Column('D', Integer),
                        Column('Артикул', Integer),
                        Column('Модель', TEXT),
                        Column('Тек_п', Integer),
                        Column('Текущая_ц', Integer),
                        Column('Себестоимость', Integer),
                        Column('Есть_огрч', TEXT),
                        Column('Ограничитель', TEXT),
                        Column('Город_1', TEXT),
                        Column('Город_1_мин_ц', Integer),
                        Column('Город_1_макс_ц', Integer),
                        Column('Город_2', TEXT),
                        Column('Город_2_мин_ц', Integer),
                        Column('Город_2_макс_ц', Integer),
                        Column('Город_3', TEXT),
                        Column('Город_3_мин_ц', Integer),
                        Column('Город_3_макс_ц', Integer),
                        Column('Город_4', TEXT),
                        Column('Город_4_мин_ц', Integer),
                        Column('Город_4_макс_ц', Integer),
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
