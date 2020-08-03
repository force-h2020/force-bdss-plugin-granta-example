import datetime

from traits.api import Instance, List

from force_bdss.api import (
    MCOStartEvent,
    MCOFinishEvent,
    MCOProgressEvent
)

from granta_example.core.base_classes import (
    BaseGrantaNotificationListener)

from .example_notification_listener_model import (
    ExampleNotificationListenerModel)


class ExampleNotificationListener(BaseGrantaNotificationListener):

    _model = Instance(ExampleNotificationListenerModel)

    _names = List()

    _values = List()

    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            self._names = list(event.input_names + event.output_names)
        elif isinstance(event, MCOProgressEvent):
            self._values.append(list(event.input + event.output))
        elif isinstance(event, MCOFinishEvent):
            self._submit_data()
        else:
            pass

    def _submit_data(self):
        """Submits the data to the GRANTA database"""
        model = self._model
        table = self._mi.get_db(db_key=model.db_key).get_table(
            model.table_name)

        curtime = datetime.datetime.now()
        parent = table
        sn = "Optimization_"+curtime.strftime('%Y-%m-%d %H:%M:%S')

        with self._mi.make_writer() as writer:
            data = {}
            writer.make_record(
                sn, parent, data, subset_names=[model.subset_name])

        parent = table.records_with_name(sn)[0]
        with self._mi.make_writer() as writer:
            for index, row in enumerate(self._values):
                if len(row) != len(self._names):
                    raise ValueError(
                        "Inconsistent size between names and values")

                named_row = dict(zip(self._names, row))
                point = "Point_"+str(index)
                data = {
                    "Concentration e": named_row[model.concentration_e_name],
                    "Material Cost": named_row[model.material_cost_name],
                    "Production Cost": named_row[model.production_cost_name],
                    "Date of Analysis": curtime.strftime('%Y-%m-%d'),
                    "Reaction Time": named_row[model.reaction_time_name],
                    "Volume a tilde": named_row[model.volume_a_tilde_name],
                    "Impurity Concentration":
                        named_row[model.impurity_concentration_name],
                    "Temperature": named_row[model.temperature_name]
                }
                writer.make_record(
                    point,
                    parent,
                    data,
                    subset_names=[model.subset_name]
                )

    def initialize(self, model):
        super().initialize(self, model)
        self._model = model

    def finalize(self):
        self._model = None
