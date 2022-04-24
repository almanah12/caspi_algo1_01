import os
from datetime import datetime
import pandas as pd
from caspi_pars.enums import all_temp_data, all_perm_data
from caspi_pars.helpers import resource_path, logger
from caspi_pars.db_tables import session, permanent_table


def check_promotion(path_to_folder):
    while True:
        if len(os.listdir(resource_path(fr"data_files/{path_to_folder}"))) != 0 \
                and os.path.exists(resource_path(fr"data_files/{path_to_folder}")):
            for root, dir, files in os.walk(resource_path(fr"data_files/{path_to_folder}")):
                logger.debug(files)
                files = sorted(files)
                logger.debug(files)

                data_cat_comm_first_file = [file for file in files][0]

            print(path_to_folder, data_cat_comm_first_file)

            year_file = int(data_cat_comm_first_file.split('_')[0])
            month_file = int(data_cat_comm_first_file.split('_')[1])
            day_file = int(data_cat_comm_first_file.split('_')[2])
            date_work = datetime(year_file, month_file, day_file)

            # ntpCllient = ntplib.NTPClient()
            # res = ntpCllient.request('pool.ntp.org')

            # date_6 = datetime(2022, 4, 9)
            # date_7 = datetime(2022, 4, 8, 23, 00, 00)
            #
            # print(date_6.timestamp() - date_7.timestamp())

            def change_price():
                d_pr = pd.read_excel(resource_path(
                    fr'data_files/{path_to_folder}/{data_cat_comm_first_file}'),
                    sheet_name=0)
                name_category = d_pr['Name category'].tolist()
                value_comm = d_pr['Value commission'].tolist()
                articuls = [row.Артикул for row in all_perm_data]

                for i in range(len(articuls)):
                    curr_row = session.query(permanent_table).filter(permanent_table.c.Артикул == articuls[i]).one()
                    count_cities = len(all_temp_data[0]['Все_города'].split(', '))
                    for k in range(len(name_category)):
                        comm = (value_comm[k] - int(curr_row['Comm'].split('%')[0])) / 100 + 1

                        # Проверят если категория определеннго товара в рассрочке
                        for itemprop_n in range(1, 4):
                            if curr_row['Категория' + str(itemprop_n)] in name_category:
                                for city_i in range(count_cities):
                                    if curr_row['Тек_ц' + str(city_i + 1)]:
                                        logger.debug(curr_row['Тек_ц' + str(city_i + 1)])
                                        write_data(city_i, curr_row, comm, path_to_folder)

                path = resource_path(fr'data_files/{path_to_folder}/{data_cat_comm_first_file}')
                os.remove(path)

            is_time_change_price = date_work.timestamp() - datetime.now().timestamp()
            logger.debug(is_time_change_price)

            if path_to_folder == 'data_cat_comm_start':
                if 3600 <= is_time_change_price <= 21600: # от 18:00 до 23:00 наступающего.дня
                    change_price()

                elif is_time_change_price < 3600:
                    logger.debug('delete file ')
                    path = resource_path(fr'data_files/{path_to_folder}/{data_cat_comm_first_file}')
                    os.remove(path)
                else:
                    break
            else:
                if -138600 <= is_time_change_price <= -109800: # от 6:30 до 14:30 след.дня
                    change_price()
                elif is_time_change_price < -138600:
                    path = resource_path(fr'data_files/{path_to_folder}/{data_cat_comm_first_file}')
                    os.remove(path)
                else:
                    break

        else:
            break


def write_data(city_i, curr_row, comm, path):
    # Для рассрочек которые начнутся
    if path == 'data_cat_comm_start':
        curr_price = int(curr_row['Тек_ц' + str(city_i + 1)]*comm)
        first_price = int(curr_row['Сбстоимость' + str(city_i + 1)] * comm)
        min_price = int(curr_row['Мин_ц' + str(city_i + 1)] * comm)
        max_price = int(curr_row['Макс_ц' + str(city_i + 1)] * comm)
    # Для рассрочек которые закончились
    else:
        curr_price = int(curr_row['Тек_ц' + str(city_i + 1)]/comm)
        first_price = int(curr_row['Сбстоимость' + str(city_i + 1)] / comm)
        min_price = int(curr_row['Мин_ц' + str(city_i + 1)] / comm)
        max_price = int(curr_row['Макс_ц' + str(city_i + 1)] / comm)

    session.query(permanent_table).filter(permanent_table.c.Артикул == curr_row['Артикул']).update(
        {'Тек_ц' + str(city_i + 1): curr_price},
        synchronize_session=False
    )

    session.query(permanent_table).filter(permanent_table.c.Артикул == curr_row['Артикул']).update(
        {'Сбстоимость' + str(city_i + 1): first_price},
        synchronize_session=False
    )

    session.query(permanent_table).filter(permanent_table.c.Артикул == curr_row['Артикул']).update(
        {'Мин_ц' + str(city_i + 1): min_price},
        synchronize_session=False
    )

    session.query(permanent_table).filter(permanent_table.c.Артикул == curr_row['Артикул']).update(
        {'Макс_ц' + str(city_i + 1): max_price},
        synchronize_session=False
    )
    session.commit()


# check_promotion('data_cat_comm_start')
# check_promotion('data_cat_comm_end')



