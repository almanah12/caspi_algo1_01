from caspi_pars.enums import all_perm_data, count_cities


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
    id = 0
    if gui.filter_comboBox.currentText() == 'Товары без данных':
        if gui.configuration.same_price_citiesradioButton.isChecked():
            for row_d in all_perm_data:
                check_dt_fill = True
                for city_c in range(count_cities):
                    if row_d['Город_' + str(city_c + 1)]:
                        check_data_fill = all(
                            [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                             row_d['Макс_ц' + str(city_c + 1)]])
                        check_dt_fill *= check_data_fill
                        break
                if check_dt_fill:
                    table.setRowHidden(id, True)
                id += 1
        else:
            for row_d in all_perm_data:
                check_dt_fill = True
                for city_c in range(count_cities):
                    if row_d['Город_' + str(city_c + 1)]:
                        check_data_fill = all(
                            [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                             row_d['Макс_ц' + str(city_c + 1)]])
                        check_dt_fill *= check_data_fill
                if check_dt_fill:
                    table.setRowHidden(id, True)
                id += 1

    if gui.filter_comboBox.currentText() == 'Товары с данными':
        if gui.configuration.same_price_citiesradioButton.isChecked():
            for row_d in all_perm_data:
                check_dt_fill = True
                for city_c in range(count_cities):
                    if row_d['Город_' + str(city_c + 1)]:
                        check_data_fill = all(
                            [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                             row_d['Макс_ц' + str(city_c + 1)]])
                        check_dt_fill *= check_data_fill
                        break
                if not check_dt_fill:
                    table.setRowHidden(id, True)
                id += 1
        else:
            for row_d in all_perm_data:
                check_dt_fill = True
                for city_c in range(count_cities):
                    if row_d['Город_' + str(city_c + 1)]:
                        check_data_fill = all(
                            [row_d['Сбстоимость' + str(city_c + 1)], row_d['Мин_ц' + str(city_c + 1)],
                             row_d['Макс_ц' + str(city_c + 1)]])
                        check_dt_fill *= check_data_fill
                if not check_dt_fill:
                    table.setRowHidden(id, True)
                id += 1

