from os import listdir
import pandas as pd

from db_tables import session, permanent_table, temporary_table
from helpers import resource_path


class ProcessingData:
    delivery_shops: object
    name_shops: object
    price_shops: object
    curr_artikul: object
    city_number: object
    curr_row: object
    limiter: object

    def __init__(self, gui, activ_moni):
        self.gui = gui
        self.activ_moni = activ_moni
        self.name_our_store = self.gui.configuration.name_store_comboBox.currentText()
        self.change_pr = self.gui.configuration.interval_change_price_spinBox.value()

    def processing_dt(self):

        shops_data_list = listdir(resource_path(r'data_files/data_shops'))
        previous_articul = 0
        for i in shops_data_list:
            # try:
            self.activ_moni.emit('Обработка ' + i + ' файла...', 1)
            # Присваевает нужные ексел файлы обьекту d_sh
            d_sh = pd.read_excel(resource_path(fr'data_files/data_shops/{i}'),
                                 sheet_name=0)
            # Присваевает обьекту name_shops все имена магазов
            self.name_shops = d_sh['Name shops'].tolist()
            self.delivery_shops = d_sh['Delivery_day'].tolist()
            self.price_shops = d_sh['Price'].tolist()
            self.curr_artikul = i.split('-')[0]
            self.city_number = i.split('_')[2].split('.')[0]
            self.curr_row = session.query(permanent_table).filter(
                permanent_table.c.Артикул == self.curr_artikul).one()
            self.limiter = self.curr_row['Огранич_?']

            # Для опредления положения магаза и занесения его в базу
            for k in range(len(getattr(self, 'name_shops'))):
                if self.name_shops[k] == self.name_our_store:
                    session.query(permanent_table).filter(permanent_table.c.Артикул == self.curr_artikul).update(
                        {'Тек_#': k+1}, synchronize_session=False)
                    session.commit()
                    break
            #
            if self.name_our_store in self.name_shops:
                # Одна цена для всех городов
                if self.gui.configuration.same_price_citiesradioButton.isChecked():
                    """
                    Условие выбирает только один город для одного товара. Цена этого города
                    выставляется  для всех городов
                    """
                    # Не допускает другие города в цикл(Город_1 для всех городов)
                    if self.curr_artikul != previous_articul:
                        previous_articul = self.curr_artikul
                        if self.limiter == "Нет":
                            self.limiter_no()
                        else:
                            self.limiter_yes()
                # Разные цены для всех городов
                else:
                    """
                      Условие выбирает разные цены для городов. выставляется Цена. разные цены
                      для всех городов
                    """
                    if self.limiter == "Нет":
                        self.limiter_no()
                    else:
                        self.limiter_yes()

                self.activ_moni.emit('Файл ' + i + ' успешно обработан', 1)

            # Если нету нашего магаза в списке
            else:
                self.activ_moni.emit("Наш магазин отсуствует у данного товара " + str(self.curr_artikul), 3)
                new_price = self.curr_row['Текущая_ц']
                competitor = "Магазин отсуствует у данного товара"
                self.write_data(new_price, competitor)

    # Ограничитель нет
    def limiter_no(self):
        # Цикл для прогона всех магазов
        for k in range(len(getattr(self, 'name_shops'))):
            # Если назв.магаза не равно назв. нашего магаза
            if self.name_shops[k] != self.name_our_store:
                # Учитывать сроки доставки
                if self.gui.configuration.consider_deliver_times_comboBox.currentText() == 'Да':
                    # Если доставка сегодня или завтра то это конкурент - заходим в усл.
                    if self.delivery_shops[k] == "сегодня," or self.delivery_shops[k] == "завтра,":
                        # Если в диапазоне мин и макс цены
                        if self.check_price_in_minmax_no(k):
                            break

                elif self.gui.configuration.consider_deliver_times_comboBox.currentText() == 'Нет':
                    # Если в диапазоне мин и макс цены
                    if self.check_price_in_minmax_no(k):
                        break

            # Если назв.магаз равно нашему магазу
            elif self.name_shops[k] == self.name_our_store:
                # Если цена не ниже себестоимости
                if self.check_price_in_minmax_no(k):
                    # Если конкурента не найден и магаз в конце списка или вовсе один в списке
                    if (k == len(self.name_shops) - 1) or k == len(self.name_shops):
                        new_price = self.price_shops[k]
                        competitor = "Нет конк. преж.цена"
                        self.write_data(new_price, competitor)
                        break

                    # Если конкурента нет и после нашего есть магаз
                    elif k < len(self.name_shops) - 1 and k != 0:
                        new_price = self.price_shops[k]
                        competitor = "Нет конк. преж.цена"
                        self.write_data(new_price, competitor)
                        break

                    # Если наш магазин первый в списке
                    elif k < len(self.name_shops) - 1 and k == 0:
                        # Поднят цену к цене конк.
                        if self.gui.configuration.up_price_to_competitor_comboBox.currentText() == 'Да':
                            new_price = self.price_shops[k + 1] - self.change_pr
                            competitor = "Поднятие к цене конк:" + self.name_shops[k + 1]
                            self.write_data(new_price, competitor)
                            break
                        # Не поднимать цену к цене конк.
                        elif self.gui.configuration.up_price_to_competitor_comboBox.currentText() == 'Нет':
                            new_price = self.price_shops[k]
                            competitor = "Нет конк. преж.цена"
                            self.write_data(new_price, competitor)
                            break
                else:
                    try:
                        price_min = self.curr_row['Город_' + str(self.city_number) + '_мин_ц']
                        new_price = price_min
                        check_price_min = price_min - 1
                        competitor = 'Текущ.цена в не диапазоне мин. и макс.ц'
                        self.write_data(new_price, competitor)
                        self.activ_moni.emit("Test", 1)
                        break
                    except:
                        price_min1 = self.curr_row['Город_1_мин_ц']
                        new_price = price_min1
                        competitor = 'Текущ.цена в не диапазоне мин. и макс.ц'
                        self.write_data(new_price, competitor)
                        self.activ_moni.emit("Testerrror", 1)
                        break

    # Ограничитель есть
    def limiter_yes(self):
        name_limiter = self.curr_row['Ограничитель']
        if name_limiter in self.name_shops:
            # Цикл для прогона всех магазов
            for k in range(len(self.name_shops)):
                if self.name_shops[k] == name_limiter:
                    self.check_price_in_minmax_yes(k)
        else:
            self.limiter_no()

    def check_price_in_minmax_no(self, k):
        """
       try - Выполняется условие когда есть мин и макс цены для всех городов.
       exsept - Выполняется условие когда поставлен галочка разные цены для всех городов, и если в остальных
       городах нету мин и макс цены. В таком случае возникает ошибка и наш exsept берет за мин и макс цены из
       первого города.
       k - номер магаза который обрабатывается:
       num_c - номер города:
       """
        try:
            price_min = self.curr_row['Город_' + str(self.city_number) + '_мин_ц']
            price_max = self.curr_row['Город_' + str(self.city_number) + '_макс_ц']
            if price_min <= self.price_shops[k] <= price_max:
                new_price = self.price_shops[k] - self.change_pr
                competitor = self.name_shops[k]
                self.write_data(new_price, competitor)
                return True
        except:
            price_min1 = self.curr_row['Город_1_мин_ц']
            price_max1 = self.curr_row['Город_1_макс_ц']
            if price_min1 <= self.price_shops[k] <= price_max1:
                new_price = self.price_shops[k] - self.change_pr
                competitor = self.name_shops[k]
                self.write_data(new_price, competitor)
                return True

    def check_price_in_minmax_yes(self, k):
        try:
            if self.curr_row['Город_' + str(self.city_number) + '_мин_ц'] < self.price_shops[k]:
                new_price = self.price_shops[k] + self.change_pr
                self.write_data(new_price, 'Цена после огр.')
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_Конк': 'Цена после огр.'}, synchronize_session=False)
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_новая_ц': new_price}, synchronize_session=False)
                # session.commit()
                return True

            elif self.curr_row['Город_' + str(self.city_number) + '_мин_ц'] > self.price_shops[k]:
                new_price = self.curr_row['Город_' + str(self.city_number) + '_мин_ц']
                self.write_data(new_price, 'Цена огр. выше нашей мин.ц')
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_Конк': 'Цена после огр.'}, synchronize_session=False)
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_новая_ц': new_price}, synchronize_session=False)
                # session.commit()
                return True

        except:
            if self.curr_row['Город_1_мин_ц'] < self.price_shops[k]:
                new_price = self.price_shops[k] + self.change_pr
                self.write_data(new_price, 'Цена после огр.')
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_Конк': 'Цена после огр.'}, synchronize_session=False)
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_новая_ц': new_price}, synchronize_session=False)
                # session.commit()
                return True
            elif self.curr_row['Город_1_мин_ц'] > self.price_shops[k]:
                new_price = self.curr_row['Город_1_мин_ц']
                self.write_data(new_price, 'Цена огр. выше нашей мин.ц')
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_Конк': 'Цена после огр.'}, synchronize_session=False)
                # session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
                #     {'Город_' + str(self.city_number) + '_новая_ц': new_price}, synchronize_session=False)
                # session.commit()
                return True

    def write_data(self, new_price, competitor):
        session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
            {'Город_' + str(self.city_number) + '_Конк': competitor}, synchronize_session=False)
        session.query(temporary_table).filter(temporary_table.c.Артикул == self.curr_artikul).update(
            {'Город_' + str(self.city_number) + '_новая_ц': new_price}, synchronize_session=False)
        session.commit()
