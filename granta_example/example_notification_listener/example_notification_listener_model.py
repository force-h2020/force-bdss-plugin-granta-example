from traits.api import Str

from granta_example.core.base_classes import (
    BaseGrantaNotificationListenerModel)


class ExampleNotificationListenerModel(BaseGrantaNotificationListenerModel):

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
