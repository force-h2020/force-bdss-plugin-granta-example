from force_bdss.api import BaseExtensionPlugin, plugin_id

from .example_notification_listener import ExampleNotificationListenerFactory
from .example_data_source import ExampleDataSourceFactory

PLUGIN_VERSION = 0


class GrantaPlugin(BaseExtensionPlugin):
    """
    """
    id = plugin_id("granta", "granta_example", PLUGIN_VERSION)

    def get_name(self):
        return u"GRANTA MI"

    def get_description(self):
        return u"Support for GRANTA MI database access."

    def get_version(self):
        return PLUGIN_VERSION

    def get_factory_classes(self):
        return [
            ExampleDataSourceFactory,
            ExampleNotificationListenerFactory
        ]
