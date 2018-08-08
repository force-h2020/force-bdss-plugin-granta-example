from traits.api import Int, Unicode, Password, on_trait_change
from traitsui.api import View, Item

from force_bdss.api import BaseDataSourceModel


class ExampleDataSourceModel(BaseDataSourceModel):
    """This model contains the data that the data source
    needs to perform its work. It is information that is
    outside the pipeline system. Example of this information
    could be, for example, authentication data (login/password)
    to a database data source. They are configured when constructing
    your workflow and do not change as the workflow is computed.
    """

    url = Unicode("https://212.44.35.85/mi_servicelayer/")
    login = Unicode()
    password = Password()
    domain = Unicode()
    attribute_name = Unicode("PRESSURE")
    row = Int(1)
    column = Int(1)

    db_key = Unicode('MI_Force')
    source_data_table_name = Unicode('Source Data')

    cuba_type_out = Unicode("PRESSURE")

    @on_trait_change("cuba_type_out")
    def _notify_changes_slots(self):
        self.changes_slots = True

    def default_traits_view(self):
        return View(
            Item("url"),
            Item("login"),
            Item("password"),
            Item("attribute_name"),
            Item("row"),
            Item("column"),
            Item("db_key"),
            Item("source_data_table_name"),
            Item("cuba_type_out")
        )
