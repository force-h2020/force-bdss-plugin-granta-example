from traits.api import Int, Unicode, Password, on_trait_change, Float
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

    db_key = Unicode('MI_FORCE_TESTING')
    url = Unicode('https://212.44.35.85/mi_servicelayer/')
    login = Unicode()
    password = Password()
    domain = Unicode("PLANETARIUM")
    table_name = Unicode("Reaction Kinetics")

    cuba_type_out = Unicode("ARRHENIUS_DELTA_H")

    traits_view = View(
        Item("url"),
        Item("login"),
        Item("password"),
        Item("db_key"),
        Item("domain"),
        Item("table_name"),
        Item("cuba_type_out")
    )

    @on_trait_change("cuba_type_out")
    def _notify_changes_slots(self):
        self.changes_slots = True