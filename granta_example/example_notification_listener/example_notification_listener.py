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
    """The notification listener will receive events as provided
    by the force_bdss API.
    At the moment, the following events are reported:

    MCOStartEvent: Emitted when the MCO has just started.
    MCOProgressEvent: Emitted when the MCO has generated
    a point that is a relevant result worth of output.
    MCOFinishEvent: Emitted when the MCO has concluded its
    execution.
    """

    _model = Instance(ExampleNotificationListenerModel)
    _session = Instance(requests.Session)
    _values = List

    #: This method must be reimplemented.
    #: It is called with an event as an argument.
    #: This implementation just prints the name of the event class.
    #: and its contents (if available). Each event carries a specific
    #: payload that can be extracted.
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
            record_name = curtime
            packet[self._model.analysis_date_attribute_name] = curdate
            packet["KPI 1"] = value[0]
            packet["KPI 1"] = value[1]
            mi.storeResults(
                self._session,
                self._model.url,
                self._model.db_key,
                self._model.test_results_table_name,
                self._model.test_results_import_folder_name,
                self._model.test_results_subset_name,
                record_name,
                packet)

    #: You are not required to override these methods.
    #: They are executing when the BDSS starts up (or ends) and can be
    #: used to setup a database connection once and for all.
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
