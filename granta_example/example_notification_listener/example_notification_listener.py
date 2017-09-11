from __future__ import print_function
import datetime

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
    sourceDataTableName = 'Source Data'
    testResultsTableName = 'Test Results'
    testResultsImportFolderName = 'Runs'

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
        parent_rec = gdlu.FindRecord(
            self.session,
            self.db_key,
            self.test_results_table_name,
            self.test_results_import_folder_name)

        fdw = gdlu.FunctionalDataWriter(
            session=self.session,
            attributeName="Plot",
            tableName=self.test_results_table_name,
            db_key=self.db_key)

        for x, y in values:
            fdw.AddPoint([x, y])

        series = fdw.CreateSeries()

        importer = gdlu.Importer(
            self.db_key,
            self.test_results_table_name,
            self.session,
            [self.test_results_table_name]
        )

        importer.AddAttribute("Plot", series)
        importer.AddAttribute("Date of Analysis", gdl.DateDataType(
            value=datetime.datetime.now().strftime('%Y-%m-%d')))

        importer.ExecuteRequest(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            parent_rec.recordReference)

    #: You are not required to override these methods.
    #: They are executing when the BDSS starts up (or ends) and can be
    #: used to setup a database connection once and for all.
    def initialize(self, model):
        domain, username = model.domain_username.split("\\")
        self.session = gdl.GRANTA_MISession(
            model.url,
            username=username,
            domain=domain,
            password=model.password
            )

    def finalize(self):
        print("Finalizing")
