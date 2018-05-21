from __future__ import print_function
import datetime
import requests
import granta_example.mipy as mi
from traits.api import Instance, List

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
    _session = Instance(requests.Session)
    _values = List

    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            self._values = []
        elif isinstance(event, MCOProgressEvent):
            self._values.append((event.input[0], event.output[0]))
        elif isinstance(event, MCOFinishEvent):
            self._submit_data(self._values)
        else:
            pass

    def _submit_data(self, values):
        """Submits the data to the GRANTA database"""
        curtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        curdate = datetime.datetime.now().strftime('%Y-%m-%d')
        packet = {}
        for index, value in enumerate(values):
            record_name = curdate+"-"+str(index)
            packet[self._model.analysis_date_attribute_name] = curdate
            packet["KPI 1"] = value[0]
            packet["KPI 2"] = value[1]
            mi.storeResults(
                self._session,
                self._model.url,
                self._model.db_key,
                self._model.test_results_table_name,
                self._model.test_results_import_folder_name,
                self._model.test_results_subset_name,
                record_name,
                packet)

    def initialize(self, model):
        self._model = model
        self._session = requests.Session()
        self._session.auth = (model.login, model.password)
        self._session.headers.update({
            'content-type': 'text/xml;charset=UTF-8'
        })

    def finalize(self):
        self._model = None
        self._session.close()
