from traits.api import Str, Password
from traitsui.api import View, Item
from force_bdss.api import BaseNotificationListenerModel


class ExampleNotificationListenerModel(BaseNotificationListenerModel):
    url = Str('https://force.grantami.com/mi_servicelayer/')
    login = Str()
    password = Password()
    db_key = Str('MI_FORCE')
    test_results_table_name = Str('Test Results')
    test_results_subset_name = Str("Test Results")
    test_results_import_folder_name = Str('Runs')
    analysis_date_attribute_name = Str("Date of Analysis")

    def default_traits_view(self):
        return View(
            Item("url"),
            Item("login"),
            Item("password"),
            Item("db_key"),
            Item("test_results_table_name"),
            Item("test_results_subset_name"),
            Item("test_results_import_folder_name"),
            Item("analysis_date_attribute_name")
        )
