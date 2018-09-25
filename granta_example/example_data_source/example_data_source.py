import logging
import granta

from force_bdss.api import BaseDataSource, Slot, DataValue

logger = logging.getLogger(__name__)


class ExampleDataSource(BaseDataSource):
    def run(self, model, parameters):
        mi = granta.MI(model.url, user_name=model.login, password=model.password, domain=model.domain)
        my_table = mi.get_db(db_key=model.db_key).get_table(model.table_name)
        reaction = list(my_table.records_where(("Product", granta.SearchOps.CONTAINS, 'P')))[0]
        delta_h_main=0
        for attribute in reaction.attributes:
            if attribute.name == "Arrhenius DeltaH main":
                delta_h_main = attribute.value[0]
        return [
            DataValue(type="ARRHENIUS_DELTA_H",
                      value=delta_h_main)
        ]

    def slots(self, model):
        return (
            (
            ),
            (
                Slot(type=model.cuba_type_out,
                     description="Arrhenius delta H parameter "
                                 "for the main reaction"
                     ),
            )
        )
