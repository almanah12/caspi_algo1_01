import xml.etree.ElementTree as xml


from db_tables import conn_engine, temp_table_select
from enums import code_cities
from helpers import resource_path


def create_xml(gui):
    data_temp_table = conn_engine.execute(temp_table_select)
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

    for row in data_temp_table:
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

        # Если цена одна для всех городов
        if gui.configuration.same_price_citiesradioButton.isChecked():
            price = xml.SubElement(offer, 'price')
            price.text = str(row.Город_1_новая_ц)

        # Если цена разные для всех городов
        else:
            cityprices = xml.Element('cityprices')
            offer.append(cityprices)
            # дОБАВЛЯЕТСЯ СУБЭЛЕменты пока условие истинно
            if row.Колич_городов > 0:
                cityprice = xml.SubElement(cityprices, 'cityprice', cityId=code_cities[row.Город_1])
                cityprice.text = str(row.Город_1_новая_ц)
            if row.Колич_городов > 1:
                cityprice = xml.SubElement(cityprices, 'cityprice', cityId=code_cities[row.Город_2])
                cityprice.text = str(row.Город_2_новая_ц)
            if row.Колич_городов > 2:
                cityprice = xml.SubElement(cityprices, 'cityprice', cityId=code_cities[row.Город_3])
                cityprice.text = str(row.Город_3_новая_ц)
            if row.Колич_городов > 3:
                cityprice = xml.SubElement(cityprices, 'cityprice', cityId=code_cities[row.Город_4])
                cityprice.text = str(row.Город_4_новая_ц)

    tree = xml.ElementTree(kaspi_catalog)
    tree.write(resource_path(r'data_shop/alash.xml'))

