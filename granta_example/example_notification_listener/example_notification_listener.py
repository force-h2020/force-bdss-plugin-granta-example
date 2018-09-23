import datetime
import granta
from traits.api import Instance, List, Any

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
        print('submitting data')
        model = self._model
        print (self._mi.dbs)
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
                data = {}
                for kpi_name in model.kpi_names:
                    data[kpi_name] = named_row[kpi_name]
                    data[kpi_name+'_weight'] = named_row[kpi_name]
                for input_name in model.input_names:
                    data[input_name] = named_row[input_name]
                # data = {
                #     "Concentration e": named_row[model.concentration_e_name],
                #     "Material Cost": named_row[model.material_cost_name],
                #     "Production Cost": named_row[model.production_cost_name],
                #     "Date of Analysis": curtime.strftime('%Y-%m-%d'),
                #     "Reaction Time": named_row[model.reaction_time_name],
                #     "Volume a tilde": named_row[model.volume_a_tilde_name],
                #     "Impurity Concentration":
                #         named_row[model.impurity_concentration_name],
                #     "Temperature": named_row[model.temperature_name]
                # }

                writer.make_record(
                    point,
                    parent,
                    data,
                    subset_names=[self._model.subset_name]
                )
        print('submitting data done')

    def initialize(self, model):
        print('Init')
        self._model = model
        self._mi = granta.MI(
            model.url,
            user_name=model.login,
            password=model.password,
            domain=model.domain)

    def finalize(self):
        self._model = None
