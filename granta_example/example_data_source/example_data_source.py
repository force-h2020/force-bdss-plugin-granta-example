import logging
import granta

from traits.api import Any
from force_bdss.api import BaseDataSource, Slot, DataValue

logger = logging.getLogger(__name__)


class ExampleDataSource(BaseDataSource):
    # _model = Instance(ExampleDataSourceModel)
    _mi = Any()

    def run(self, model, parameters):

        mi = granta.MI(
            model.url, user_name=model.login, password=model.password,
            domain=model.domain
        )
        my_table = mi.get_db(db_key=model.db_key).get_table(model.table_name)
        reaction_list = list(my_table.records_where((
            "Product", granta.SearchOps.CONTAINS, 'P')))
        reaction = reaction_list[0]
        attribute_names = []
        for attribute in reaction.attributes:
            attribute_names.append(attribute.name)
            if attribute.name == "Arrhenius DeltaH main":
                delta_h_main = attribute.value[0]
        if "Arrhenius DeltaH main" not in attribute_names:
            raise ValueError('Arrhenius DeltaH main was not '
                             'found in the external database')
        return [DataValue(type="ARRHENIUS_DELTA_H", value=delta_h_main)]

    def slots(self, model):
        return (
            tuple(),
            tuple(Slot(type=model.cuba_type_out,
                       description="Arrhenius delta H parameter "
                                 "for the main reaction"
                       ),
                 )
            )
