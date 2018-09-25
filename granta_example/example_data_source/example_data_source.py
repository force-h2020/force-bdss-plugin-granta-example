import logging
import granta

from traits.api import Instance, Any
from force_bdss.api import BaseDataSource, Slot, DataValue
from granta_example.example_data_source.example_data_source_model import ExampleDataSourceModel

logger = logging.getLogger(__name__)


class ExampleDataSource(BaseDataSource):
    # _model = Instance(ExampleDataSourceModel)
    _mi = Any()

    def run(self, model, parameters):

        # model = self._model

        # Set up MI database instance
        self._mi = granta.MI(model.url,
                             user_name=model.login,
                             password=model.password,
                             domain=model.domain)

        table = self._mi.get_db(db_key=model.db_key.get_table(model.source_data_table_name))

        data_records = table.records_with_name('reactor_volume')

        reactor_volume = data_records.get_attribute('reactor_volume')
        
        return [
            DataValue(
                type=model.cuba_type_out,
                value=reactor_volume
            )]

    def slots(self, model):
        return (
            (
            ),
            (
                Slot(type='VOLUME',
                     description='Reactor Volume'),
            )
        )
