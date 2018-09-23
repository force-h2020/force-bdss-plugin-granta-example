from traits.api import Unicode, Password, List
from traitsui.api import View, Item
from force_bdss.api import BaseNotificationListenerModel


class ExampleNotificationListenerModel(BaseNotificationListenerModel):
    url = Unicode('https://212.44.35.85/mi_servicelayer/')
    login = Unicode()
    password = Password()
    domain = Unicode()
    db_key = Unicode('MI_Force')
    table_name = Unicode('Optimization Tests')
    subset_name = Unicode("Optimization Tests")

    # Input params
    volume_a_tilde_name = Unicode()
    concentration_e_name = Unicode()
    reaction_time_name = Unicode()
    temperature_name = Unicode()
    input_names = List(Unicode)

    # KPIs
    material_cost_name = Unicode()
    production_cost_name = Unicode()
    impurity_concentration_name = Unicode()
    kpi_names = List(Unicode)

    def default_traits_view(self):
        return View(
            Item("url"),
            Item("login"),
            Item("password"),
            Item("domain"),
            Item("db_key"),
            Item("table_name"),
            Item("subset_name"),

            Item("volume_a_tilde_name"),
            Item("concentration_e_name"),
            Item("reaction_time_name"),
            Item("temperature_name"),

            # KPIs
            Item("material_cost_name"),
            Item("production_cost_name"),
            Item("impurity_concentration_name"),
        )

    def _kpi_names_default(self):
        return [self.material_cost_name, self.production_cost_name,
                self.impurity_concentration_name]

    def _input_names_default(self):
        return [self.volume_a_tilde_name, self.concentration_e_name,
                self.reaction_time_name, self.temperature_name]