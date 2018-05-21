from force_bdss.api import BaseExtensionPlugin, plugin_id

from .example_notification_listener import ExampleNotificationListenerFactory
from .example_data_source import ExampleDataSourceFactory


class ExamplePlugin(BaseExtensionPlugin):
    """
    """
    id = plugin_id("granta", "granta_example", 0)

    def get_factory_classes(self):
        return [
            ExampleDataSourceFactory,
            ExampleNotificationListenerFactory
        ]
