import xml.etree.ElementTree as xml


from caspi_pars.enums import code_cities, all_temp_data
from caspi_pars.helpers import resource_path


def create_xml(gui):
    # data_temp_table = conn_engine.execute(temp_table_select)
    xmlns = "kaspiShopping"
    xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
    xsi_schemaLocation = "kaspiShopping http://kaspi.kz/kaspishopping.xsd"

    kaspi_catalog = xml.Element("kaspi_catalog", date="string", xmlns=xmlns)
    kaspi_catalog.set('xmlns', xmlns)
    kaspi_catalog.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', xsi_schemaLocation)

    company = xml.SubElement(kaspi_catalog, 'company')
    company.text = gui.configuration.name_store_comboBox.currentText()
    merchantid = xml.SubElement(kaspi_catalog, 'merchantid')
    merchantid.text = gui.configuration.id_partner_lineEdit.text()
    offers = xml.Element("offers")
    kaspi_catalog.append(offers)

    for row in all_temp_data:
        offer = xml.Element("offer", sku=str(row.Артикул))
        offers.append(offer)

        model = xml.SubElement(offer, 'model')
        model.text = row.Модель

        brand = xml.SubElement(offer, 'brand')
        brand.text = row.Брэнд

        availabilites = xml.Element('availabilities')
        offer.append(availabilites)
        list_availability = row.Доступность.split(', ')
        for i in range(len(list_availability)):
            availabilites.append(xml.Element('availability', available='yes', storeId=list_availability[i]))

        cities_c = len(row['Все_города'].split(', '))
        if not row['Scrap_st']:
            # Если цена одна для всех городов
            if gui.configuration.same_price_citiesradioButton.isChecked():
                price = xml.SubElement(offer, 'price')
                for city_n in range(cities_c):
                    if row['Город_'+str(city_n+1)]:
                        price.text = str(row['Г_{}_новая_ц'.format(str(city_n+1))])
                        break

            # Если цена разные для всех городов
            else:
                cityprices = xml.Element('cityprices')
                offer.append(cityprices)
                for city_n in range(cities_c):
                    # дОБАВЛЯЕТСЯ СУБЭЛЕменты пока условие истинно
                    if row['Город_'+str(city_n+1)]:
                        cityprice = xml.SubElement(cityprices, 'cityprice', cityId=code_cities[row['Город_'+str(city_n+1)]])
                        cityprice.text = str(row['Г_{}_новая_ц'.format(str(city_n+1))])

        # товар который не парсился. вСЕГДА ОДНА ЦЕНА ДЛЯ ВСЕХ ГОРОДОВ
        else:
            price = xml.SubElement(offer, 'price')
            price.text = str(row['Тек_ц1'])

    tree = xml.ElementTree(kaspi_catalog)
    tree.write(resource_path(r'data_shop/alash.xml'))

