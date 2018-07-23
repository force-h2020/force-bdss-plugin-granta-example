from traits.api import Str, Password
from traitsui.api import View, Item
from force_bdss.api import BaseNotificationListenerModel


class ExampleNotificationListenerModel(BaseNotificationListenerModel):
    url = Str('https://212.44.35.85/mi_servicelayer/')
    login = Str()
    password = Password()
    domain = Str()
    db_key = Str('MI_Force')
    table_name = Str('Optimization Tests')
    subset_name = Str("Optimization Tests")

    # Input params
    volume_a_tilde_name = Str()
    concentration_e_name = Str()
    reaction_time_name = Str()
    temperature_name = Str()

    # KPIs
    material_cost_name = Str()
    production_cost_name = Str()
    impurity_concentration_name = Str()

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
