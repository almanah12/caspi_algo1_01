import os

from sqlalchemy import create_engine, select, Table, Column, Integer, MetaData, TEXT, Float, String
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
                        Column('Доступность', TEXT),
                        Column('Колич_г', Integer),
                        Column('Все_города', TEXT),
                        Column('Город_1', TEXT),
                        Column('Тек_ц1', Integer),
                        Column('Г_1_Конк', TEXT),
                        Column('Г_1_новая_ц', Integer),
                        Column('Город_2', TEXT),
                        Column('Тек_ц2', Integer),
                        Column('Г_2_Конк', TEXT),
                        Column('Г_2_новая_ц', Integer),
                        Column('Город_3', TEXT),
                        Column('Тек_ц3', Integer),
                        Column('Г_3_Конк', TEXT),
                        Column('Г_3_новая_ц', Integer),
                        Column('Город_4', TEXT),
                        Column('Тек_ц4', Integer),
                        Column('Г_4_Конк', TEXT),
                        Column('Г_4_новая_ц', Integer)
                        )

# Постояная таблица куда сохраним данные товаров магаза
permanent_table = Table('permanent_table', meta,
                        Column('E', Integer),
                        Column('D', Integer),
                        Column('Артикул', Integer),
                        Column('Модель', TEXT),
                        Column('Есть_огрч', TEXT),
                        Column('Ограничитель', TEXT),  # 5
                        Column('Город_1', TEXT),
                        Column('Т_п1', Integer),
                        Column('Тек_ц1', Integer),
                        Column('Сбстоимость1', Integer),
                        Column('Мин_ц_проц1', Float),  # 10
                        Column('Мин_ц1', Integer),
                        Column('Макс_ц_проц1', Float),
                        Column('Макс_ц1', Integer),
                        Column('Город_2', TEXT),
                        Column('Т_п2', Integer),  # 15
                        Column('Тек_ц2', Integer),
                        Column('Сбстоимость2', Integer),
                        Column('Мин_ц_проц2', Float),
                        Column('Мин_ц2', Integer),
                        Column('Макс_ц_проц2', Float),  # 20
                        Column('Макс_ц2', Integer),
                        Column('Город_3', TEXT),
                        Column('Т_п3', Integer),
                        Column('Тек_ц3', Integer),
                        Column('Сбстоимость3', Integer),  # 25
                        Column('Мин_ц_проц3', Float),
                        Column('Мин_ц3', Integer),
                        Column('Макс_ц_проц3', Float),
                        Column('Макс_ц3', Integer),
                        Column('Город_4', TEXT),  # 30
                        Column('Т_п4', Integer),
                        Column('Тек_ц4', Integer),
                        Column('Сбстоимость4', Integer),
                        Column('Мин_ц_проц4', Float),
                        Column('Мин_ц4', Integer),  # 35
                        Column('Макс_ц_проц4', Float),
                        Column('Макс_ц4', Integer),
                        Column('Колич_г', Integer),

                        Column('ItemProp1', TEXT),
                        Column('ItemProp2', TEXT),
                        Column('ItemProp3', TEXT),
                        Column('Comm', Integer),
                        Column('Filter', Integer),
                        )

if not os.path.exists(resource_path('data_shop')):
    os.mkdir(resource_path('data_shop'))
    open(resource_path('data_shop/cannot_be_parsed.txt'), 'a').close()

res_path = resource_path(r'data_shop/dt_goods.sqlite')
engine = create_engine(r"sqlite:///"+res_path, connect_args={'check_same_thread': False}, poolclass=StaticPool, echo=False)

meta.create_all(engine)  # или books.create(engine), authors.create(engine)
conn_engine = engine.connect()
temp_table_select = select(temporary_table)
perm_table_select = select(permanent_table)
Session = sessionmaker(bind=engine)
session = Session()
