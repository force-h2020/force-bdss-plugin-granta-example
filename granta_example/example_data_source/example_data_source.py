import logging

from force_bdss.api import Slot

from granta_example.core.base_classes import BaseGrantaDataSource

logger = logging.getLogger(__name__)


class ExampleDataSource(BaseGrantaDataSource):

    def run(self, model, parameters):
        raise NotImplementedError("Executing ExampleDataSource. "
                                  "Currently not implemented")

    def slots(self, model):
        return (
            (
            ),
            (
                Slot(type=model.cuba_type_out),
            )
        )
