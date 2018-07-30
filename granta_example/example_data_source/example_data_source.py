import logging

from force_bdss.api import BaseDataSource, Slot

logger = logging.getLogger(__name__)


class ExampleDataSource(BaseDataSource):
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
