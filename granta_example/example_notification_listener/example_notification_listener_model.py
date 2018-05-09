from traits.api import String
from force_bdss.api import BaseNotificationListenerModel


class ExampleNotificationListenerModel(BaseNotificationListenerModel):
    """
    This class contains the information needed by the notification listener.
    For example, if your notification listener is something that contacts
    a database, you would put here traits for the credentials and the URL
    to connect. The example listener does not need any configuration, so it's
    empty.

    Note: we don't yet have a UI in place to allow configuration
    of these parameters, nor to add notification listeners to your execution.
    For now, the only way for the BDSS to use notification listeners
    is to modify the workflow file by hand.
    """
    url = String('https://force.grantami.com/mi_servicelayer/')
    login = String()
    password = String()
    db_key = String('MI_FORCE')
    source_data_table_name = String('Source Data')
    test_results_table_name = String('Test Results')
    test_results_subset_name = String("Test Results")
    test_results_import_folder_name = String('Runs')
    analysis_date_attribute_name = String("Date of Analysis")
