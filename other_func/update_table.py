# from caspi_pars.db_QSqlDatabase import model_temp, model_perm
# from caspi_pars.enums import filter_all_data, filter_for_goods_without_data, filter_for_goods_with_data
# from caspi_pars.interface.utils import add_to_data_table_view
#
#
# def update_table(self):
#     print('click')
#
#     model_temp.setFilter(filter_all_data)
#     add_to_data_table_view(self, model_perm, 'permanent_table', self.permanent_tableView)
#
#     if self.filter_comboBox.currentText() == 'Товары без данных':
#         model_perm.setFilter(filter_for_goods_without_data)
#
#     elif self.filter_comboBox.currentText() == 'Товары с данными':
#         model_perm.setFilter(filter_for_goods_with_data)
#
#     else:
#         model_perm.setFilter(filter_all_data)