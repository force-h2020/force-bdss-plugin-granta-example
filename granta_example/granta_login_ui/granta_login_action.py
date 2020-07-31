#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from pyface.api import information
from pyface.tasks.action.api import TaskAction
from traits.api import Instance

from .granta_login_view import GrantaLoginModel, GrantaLoginView


class GrantaLoginAction(TaskAction):
    """ Pop up config/login window for Granta database. """

    #: The window title
    title = 'Login to GrantaMI DB'

    #: The label for the action.
    name = '&Login to GrantaMI...'

    #: Unique ID for the action.
    id = 'GrantaLogin'

    login_model = Instance(GrantaLoginModel)

    def perform(self, event=None):
        """Opens a dialog to login to a GrantaMI database.

        Parameters
        ----------
        event : ActionEvent instance
            The event that triggered the action.
        """
        database_login = GrantaLoginView(model=self.login_model)

        parent = self.task.window.control
        success = database_login.edit_traits(
            parent=parent, kind='livemodal'
        ).result

        if not success:
            return

        msg = (
            'Connection to GrantaMI sucessful. '
        )
        information(parent=parent, message=msg)
