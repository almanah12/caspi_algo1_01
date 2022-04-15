from caspi_pars.db_QSqlDatabase import model_perm
from caspi_pars.enums import all_perm_data, count_cities, active_goods, filter_for_goods_without_data, \
    filter_for_goods_with_data
from caspi_pars.db_tables import permanent_table, session


def ch_data_fill(gui):
    check_dt_fill = True
    if gui.configuration.same_price_citiesradioButton.isChecked():
        text_warn = 'Режим "Одна цена для всех городов", заполните данные хотя бы одного города'
        for row_d in all_perm_data:
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

            for city_c in range(count_cities):
                if row_d['Город_' + str(city_c + 1)]:
                    check_data_fill = all([row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                                           row_d['Макс_ц' + str(city_c + 1)]])
                    check_dt_fill *= check_data_fill

    return [check_data_fill, text_warn]


def ch_dt_fill_for_tableview(gui, table):
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


def active_goods_table(table):
    id = 0
    for row_d in all_perm_data:
        if row_d['Артикул'] not in active_goods:
            table.setRowHidden(id, True)
        id += 1


