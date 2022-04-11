from caspi_pars.db_QSqlDatabase import model_perm
from caspi_pars.other_func.check_data_fill import ch_data_fill
from caspi_pars.db_tables import session, permanent_table
from caspi_pars.interface.utils import add_to_data_table_view
count_row_t = session.query(permanent_table.c.Артикул).count()


def filter_data(gui):
    """
    Фильтрует данные
    """
    if gui.filter_comboBox.currentText() == 'Товары без данных':
        for id in range(count_row_t):
            if not ch_data_fill(gui):
                add_to_data_table_view(gui, model_perm, 'permanent_table', gui.permanent_tableView).setRowHidden(id, True)

    elif gui.filter_comboBox.currentText() == 'Товары с данными':
        for id in range(count_row_t):
            if ch_data_fill(gui):
                print(234234234234234)

    else:
        print(12122121212121)
        # model_perm.setFilter(filter_all_data)