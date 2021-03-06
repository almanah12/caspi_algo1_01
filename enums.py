"""
Enum classes and constants.
"""
import uuid

import pandas

from caspi_pars.helpers import resource_path
from caspi_pars.db_tables import temporary_table, session, permanent_table

active_goods = []

count_cities = 4
_AppName_ = 'AlashPars'

list_stores_ini = resource_path(r'data_shop/list_stores.ini')

list_stores = ['', 'Sulpak', 'Белый Ветер', 'ALSER', 'Мечта', 'MediaPark']
list_stores = sorted(list_stores)
list_cities = ['', 'Сарыагаш', 'Алматы', 'Астана', 'Абай', 'Акколь', 'Аксай', 'Аксу', 'Актау', 'Актобе', 'Алга',
               'Алтай', 'Аральск', 'Аркалык', 'Арысь', 'Атырау', 'Аягоз', 'Байконыр', 'Балхаш', 'Бейнеу', 'Глубокое',
               'Есик', 'Жанаозен','Жаркент', 'Жезказган', 'Железинка', 'Жетыбай', 'Жетысай', 'Житикара', 'Зайсан',
               'Зачаганск', 'Капшагай', 'Караганда', 'Каратау', 'Каскелен', 'Кентау', 'Кокшетау', 'Кордай',
               'Костанай', 'Косшы', 'Кульсары', 'Курчатов', 'Курык', 'Кызылорда', 'Лисаковск', 'Нур-Султан', 'Павлодар',
               'Петропавловск', 'Риддер', 'Рудный', 'Сарань', 'Сарыагаш', 'Сатпаев', 'Семей', 'Степногорск', 'Талгар',
               'Талдыкорган', 'Тараз', 'Текели', 'Темиртау', 'Тобыл', 'Туркестан', 'Уральск', 'Усть-Каменогорск',
               'Форт-Шевченко', 'Хромтау', 'Шардара', 'Шахтинск', 'Шемонаиха', 'Шетпе', 'Шиели', 'Шу', 'Шымкент',
               'Щучинск', 'Экибастуз'
               ]

code_cities = {'Алматы': "750000000", 'Абай': "353220100", 'Акколь': "113220100", 'Аксай': "273620100", 'Аксу': "551610000", 'Актау': "471010000", 'Актобе': "151010000",
               'Алга': "153220100", 'Алтай': "634820100", 'Аральск': "433220100", 'Аркалык': "391610000", 'Арысь': "511610000", 'Атырау': "231010000", 'Аягоз': "633420100",
               'Байконыр': '431910000', 'Балхаш': '351610000', 'Бейнеу': '473630100', 'Глубокое': '634030100','Есик': '194020100', 'Жанаозен': '471810000', 'Жаркент': '195620100',
               'Жезказган': '351810000', 'Железинка': '554230100', 'Жетыбай': '474239100', 'Жетысай': '514420100', 'Житикара': "394420100", 'Зайсан': '634620100',
               'Зачаганск': '271035100', 'Капшагай': '191610000', 'Караганда': "351010000", 'Каратау': "316220100", 'Каскелен': "195220100", 'Кентау': "612010000",
               'Кокшетау': "111010000", 'Кордай': "314851205", 'Костанай': "391010000", 'Косшы': "116651100", 'Кульсары': "233620100", 'Курчатов': "632210000", 'Курык': "474230100",
               'Кызылорда': "431010000", 'Лисаковск': "392010000", 'Нур-Султан': "710000000", 'Павлодар': "551010000", 'Петропавловск': "591010000", 'Риддер': "156420100",
               'Рудный': "392410000", 'Сарань': "352210000", 'Сарыагаш': "515420100", 'Сатпаев': "352310000", 'Семей': "632810000", 'Степногорск': "111810000", 'Талгар': "196220100",
               'Талдыкорган': "191010000", 'Тараз': "311010000", 'Текели': "192610000", 'Темиртау': "352410000", 'Тобыл': "395430100", 'Туркестан': "512610000", 'Уральск': "271010000",
               'Усть-Каменогорск': "631010000", 'Форт-Шевченко': "475220100", 'Хромтау': "156020100", 'Шардара': "616420100", 'Шахтинск': "352810000", 'Шемонаиха': "636820100",
               'Шетпе': "474630100", 'Шиели': "117055900", 'Шу': "316621100", 'Шымкент': "511010000", 'Щучинск': "117020100", 'Экибастуз': "552210000"}

list_cities = sorted(list_cities)

list_PP = ('', 'PP1', 'PP2', 'PP3', 'PP4', 'PP5', 'PP6', 'PP7')
list_number_cities = ('', 'Основной город', 'Город 2', 'Город 3', 'Город 4')
filter_all_data = 'Артикул LIKE "%%"'


list_user_agents = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.3; rv:98.0) Gecko/20100101 Firefox/98.0',
                    )

dict_month = {1: 'января', 2: 'февраля', 3: 'марта',  4: 'апреля', 5: 'мая',  6: 'июня',  7: 'июля',  8: 'августа', 9: 'сентября',  10: 'октября',  11: 'ноября',  12: 'декабря'}

list_column_for_tableview = [14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 35, 37]

filter_for_goods_without_data = "Filter is NULL or Filter is ''"

filter_for_goods_with_data = "Filter LIKE 1"

all_perm_data = session.query(permanent_table)
all_temp_data = session.query(temporary_table)

curr_uuid = str(uuid.uuid1()).split('-')[4]

# telegram
token = "5186311540:AAHhIODRjVjaUhjmQVzSQwalUk3JsOHmB4E"
channel_id = "834178298"



