from caspi_pars.db_QSqlDatabase import model_perm
from caspi_pars.enums import all_perm_data, count_cities, all_temp_data
from caspi_pars.db_tables import permanent_table, session, temporary_table
from caspi_pars.threads.runThreadMethods.gets_dt_caspi_client import GetDataKaspiSeller


def ch_data_fill(gui):
    check_dt_fill = True
    if gui.configuration.same_price_citiesradioButton.isChecked():
        text_warn = 'Режим "Одна цена для всех городов", заполните данные хотя бы одного города'
        for row_d in all_perm_data:
            if row_d['Active_g']:
                for city_c in range(count_cities):
                    if row_d['Город_' + str(city_c + 1)]:
                        check_data_fill = all(
                            [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                             row_d['Макс_ц' + str(city_c + 1)]])
                        check_dt_fill *= check_data_fill
                        break
    else:
        text_warn = 'Режим "Разные цены для всех городов", заполните данные всех городов'
        for row_d in all_perm_data:
            if row_d['Active_g']:
                for city_c in range(count_cities):
                    if row_d['Город_' + str(city_c + 1)]:
                        check_data_fill = all([row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                                               row_d['Макс_ц' + str(city_c + 1)]])
                        check_dt_fill *= check_data_fill

    return [check_dt_fill, text_warn]


def ch_dt_fill_for_tableview(gui):
    filter_data_write(gui)
    gui.filter_data()


def filter_data_write(gui):
    if gui.configuration.same_price_citiesradioButton.isChecked():
        for row_d in all_perm_data:
            check_dt_fill_tb = True
            for city_c in range(count_cities):
                if row_d['Город_' + str(city_c + 1)]:
                    check_dt_fill = all(
                        [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                         row_d['Макс_ц' + str(city_c + 1)]])
                    check_dt_fill_tb *= check_dt_fill
                    break
            if check_dt_fill_tb:
                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                    {'Filter': 1}, synchronize_session=False)
            else:
                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                    {'Filter': ''}, synchronize_session=False)
            session.commit()

    else:
        for row_d in all_perm_data:
            check_dt_fill_tb = True
            for city_c in range(count_cities):
                if row_d['Город_' + str(city_c + 1)]:
                    check_dt_fill = all(
                        [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                         row_d['Макс_ц' + str(city_c + 1)]])
                    check_dt_fill_tb *= check_dt_fill

            if check_dt_fill_tb:
                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update({'Filter': 1}, synchronize_session=False)

            else:
                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                    {'Filter': ''}, synchronize_session=False)
            session.commit()


def active_goods_table():
    active_vendor_code_list = [i['Артикул'] for i in all_temp_data.filter(temporary_table.c.Артикул).all()]
    for row_d in all_perm_data:
        session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update({'Active_g': 1},
                                                                                                     synchronize_session=False)
        if row_d['Артикул'] not in active_vendor_code_list:
            session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update({'Active_g': ''},
                                                                                                        synchronize_session=False)




