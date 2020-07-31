#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from envisage.ui.tasks.tasks_plugin import TasksPlugin
from pyface.tasks.action.api import SMenu
from traits.api import List

from force_bdss.api import BaseExtensionPlugin, plugin_id

from granta_example.granta_login_ui.granta_login_action import (
    GrantaLoginAction)

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

    #: Contribution to task extensions
    contributed_task_extensions = List(
        contributes_to=TasksPlugin.TASK_EXTENSIONS,
    )

    def build_login_action(self):
        return SMenu(
            GrantaLoginAction(),
            name="&Login",
            id='Login',
        )

    def _contributed_task_extensions_default(self):
        from envisage.ui.tasks.api import TaskExtension
        from pyface.tasks.action.api import SchemaAddition

        extension = [
            TaskExtension(
                actions=[
                    SchemaAddition(
                        path='mymenu',
                        factory=self.build_login_action,
                        id='file.login.schema'
                    ),
                ],
            ),
        ]
        return extension
