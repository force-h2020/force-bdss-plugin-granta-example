import datetime
import granta
from traits.api import Instance, List, Any, on_trait_change

from force_bdss.api import (
    BaseNotificationListener,
    MCOStartEvent,
    MCOFinishEvent,
    MCOProgressEvent
)
from granta_example.example_notification_listener\
    .example_notification_listener_model import \
    ExampleNotificationListenerModel


class ExampleNotificationListener(BaseNotificationListener):
    _model = Instance(ExampleNotificationListenerModel)
    _mi = Any()
    _names = List()
    _values = List()

    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            value_names = list(event.parameter_names)
            for kpi_name in event.kpi_names:
                value_names.extend([kpi_name, kpi_name + "_weight"])
            self._names = value_names
        elif isinstance(event, MCOProgressEvent):
            data = [dv.value for dv in event.optimal_point]
            for kpi, weight in zip(event.optimal_kpis, event.weights):
                data.extend([kpi.value, weight])
            data = tuple(map(float, data))
            print('data:', data)
            self._values.append(data)
        elif isinstance(event, MCOFinishEvent):
            self._submit_data(self._values)
        else:
            pass

    def _submit_data(self, values):
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
            for index, row in enumerate(values):
                if len(row) != len(self._names):
                    raise ValueError(
                        "Inconsistent size between names and values")

                named_row = dict(zip(self._names, row))
                point = "Point_"+str(index)
                data = {}
                for kpi_name in model.kpi_names:
                    data[model.kpi_names[kpi_name]] = named_row[kpi_name]
                    data[model.kpi_names[kpi_name]+' weight'] = \
                        named_row[kpi_name+'_weight']
                for input_name in model.input_names:
                    data[model.input_names[input_name]] = named_row[input_name]
                writer.make_record(
                    point,
                    parent,
                    data,
                    subset_names=[self._model.subset_name]
                )

    def initialize(self, model):
        self._model = model
        self._mi = granta.MI(
            model.url,
            user_name=model.login,
            password=model.password,
            domain=model.domain)

    def finalize(self):
        self._model = None
