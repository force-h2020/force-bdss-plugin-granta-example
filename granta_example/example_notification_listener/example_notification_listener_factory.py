from force_bdss.api import BaseNotificationListenerFactory

from .example_notification_listener import ExampleNotificationListener
from .example_notification_listener_model import \
    ExampleNotificationListenerModel


class ExampleNotificationListenerFactory(BaseNotificationListenerFactory):
    def get_identifier(self):
        return "granta_data_submitter"

    def get_name(self):
        return "GRANTA Data Submitter"

    def get_model_class(self):
        return ExampleNotificationListenerModel

    def get_listener_class(self):
        return ExampleNotificationListener
