#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from pyface.api import information
from pyface.tasks.action.api import TaskAction
from traits.api import Instance

from .granta_login_view import GrantaLoginView
from .granta_session_manager import GrantaSessionManager


class GrantaLoginAction(TaskAction):
    """ Pop up config/login window for Granta database. """

    #: The window title
    title = 'Login to GrantaMI DB'

    #: The label for the action.
    name = '&Login to GrantaMI...'

    #: Unique ID for the action.
    id = 'GrantaLogin'

    session_manager = Instance(GrantaSessionManager)

    def perform(self, event=None):
        """Opens a dialog to login to a GrantaMI database.

        Parameters
        ----------
        event : ActionEvent instance
            The event that triggered the action.
        """
        model = self.session_manager.login_model
        database_login = GrantaLoginView(model=model)

        parent = self.task.window.control
        success = database_login.edit_traits(
            parent=parent, kind='livemodal'
        ).result

        if not success:
            return

        self.session_manager.update_session()
        msg = (
            'Connection to GrantaMI sucessful. '
        )
        information(parent=parent, message=msg)
