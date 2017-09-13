from __future__ import print_function
import datetime
import random
import requests
import mipy as mi

from force_bdss.api import (
    BaseNotificationListener,
    MCOStartEvent,
    MCOFinishEvent,
    MCOProgressEvent
)


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

    db_key = 'MI_FORCE'
    source_data_table_name = 'Source Data'
    test_results_table_name = 'Test Results'
    test_results_subset_name = "Test Results"
    test_results_import_folder_name = 'Runs'
    analysis_date_attribute_name= "Date of Analysis"
    url = 'http://force.grantami.com/mi_servicelayer/'
    session = None

    #: This method must be reimplemented.
    #: It is called with an event as an argument.
    #: This implementation just prints the name of the event class.
    #: and its contents (if available). Each event carries a specific
    #: payload that can be extracted.
    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            self.values = []
        elif isinstance(event, MCOProgressEvent):
            self.values.append((event.input[0], event.output[0]))
        elif isinstance(event, MCOFinishEvent):
            self._submit_data(self.values)
        else:
            pass

    def _submit_data(self, values):
        record_name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values[self.analysis_date_attribute_name] = datetime.datetime.now().strftime('%Y-%m-%d')
        mi.storeResults(self.session, self.url, self.db_key, self.test_results_table_name, self.test_results_import_folder_name, self.test_results_subset_name, record_name, values)

    #: You are not required to override these methods.
    #: They are executing when the BDSS starts up (or ends) and can be
    #: used to setup a database connection once and for all.
    def initialize(self, model):
        self.session = requests.Session()
        self.session.auth = (model.login, model.password)
        self.session.headers.update({'content-type':'text/xml;charset=UTF-8'})

    def finalize(self):
        print("Finalizing")
