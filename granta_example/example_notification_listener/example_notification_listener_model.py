from traits.api import Unicode, Password, List, Button, on_trait_change, Dict, Any
from traitsui.api import View, Item
from force_bdss.api import BaseNotificationListenerModel

import granta

class ExampleNotificationListenerModel(BaseNotificationListenerModel):
    url = Unicode('https://212.44.35.85/mi_servicelayer/')
    login = Unicode()
    password = Password()
    domain = Unicode()
    db_key = Unicode('MI_FORCE_TESTING')
    table_name = Unicode('Optimization Tests')
    subset_name = Unicode("Optimization Tests")

    # Input params
    volume_a_tilde_name = Unicode()
    concentration_e_name = Unicode()
    reaction_time_name = Unicode()
    temperature_name = Unicode()
    #input_names = Property(List(Unicode), depends_on='volume_a_tilde_name,concentration_e_name,reaction_time_name,'
    #                                                 'temperature_name')
    input_names = Any()

    # KPIs
    material_cost_name = Unicode()
    production_cost_name = Unicode()
    impurity_concentration_name = Unicode()
    #kpi_names = Property(List(Unicode), depends_on='material_cost_name,production_cost_name,impurity_concentration_name')
    kpi_names = Any()

    # Button
    ping_database = Button('Talk to Database')

    def default_traits_view(self):
        return View(
            Item("url"),
            Item("login"),
            Item("password"),
            Item("domain"),
            Item("db_key"),
            Item("table_name"),
            Item("subset_name"),
            Item('ping_database'),

            # Input Parameters
            Item("volume_a_tilde_name"),
            Item("concentration_e_name"),
            Item("reaction_time_name"),
            Item("temperature_name"),

            # KPIs
            Item("material_cost_name"),
            Item("production_cost_name"),
            Item("impurity_concentration_name"),
        )

    @on_trait_change('volume_a_tilde_name,concentration_e_name,reaction_time_name,temperature_name')
    def update_input(self):
        self.input_names = {self.volume_a_tilde_name:'Volume a tilde', self.concentration_e_name:'Concentration e',
                 self.reaction_time_name:'Reaction Time', self.temperature_name:'Temperature'}

    @on_trait_change('material_cost_name,production_cost_name,impurity_concentration_name')
    def update_kpi(self):
        self.kpi_names={self.material_cost_name:'Material Cost', self.production_cost_name: 'Production Cost',
                 self.impurity_concentration_name:'Impurity Concentration'}

    # def _get_kpi_names(self):
    #     return [self.material_cost_name, self.production_cost_name,
    #             self.impurity_concentration_name]
    #
    # def _get_input_names(self):
    #     return [self.volume_a_tilde_name, self.concentration_e_name,
    #             self.reaction_time_name, self.temperature_name]

    @on_trait_change('ping_database')
    def ping_database_fn(self):
        _mi = granta.MI(
            self.url,
            user_name=self.login,
            password=self.password,
            domain=self.domain)
        table = _mi.get_db(db_key=self.db_key).get_table(self.table_name)
        print(table.attributes)
