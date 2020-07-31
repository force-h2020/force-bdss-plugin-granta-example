#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Instance
from traits.has_traits import HasStrictTraits
from traitsui.api import (
    Item, ModelView, Spring, TextEditor, UItem, VGroup, View
)
from pyface.api import MessageDialog

from granta_example.core.granta_mixin_classes import (
    GrantaAuthMixin, GrantaConnectMixin)


class GrantaLoginModel(GrantaAuthMixin, GrantaConnectMixin, HasStrictTraits):

    def test_connection(self):
        try:
            self._connect_mi(self)
        except Exception as err:
            return False, err
        return True, None


class GrantaLoginView(ModelView):
    """UI used to log into a GrantaMI database."""

    #: Reference to the model class holding the login details
    model = Instance(GrantaLoginModel)

    def default_traits_view(self):

        view = View(
            VGroup(
                UItem('model.url', resizable=True),
                Item('model.domain', label='Domain (optional)'),
                Item('model.db_key', label='DB key (optional)'),
                label='Database Location',
                show_border=True,
            ),
            VGroup(
                Item('model.login'),
                Item('model.password',
                     editor=TextEditor(password=True)),
                label='User details',
            ),
            Spring(),
            width=500,
            resizable=True,
            buttons=['OK', 'Cancel'],
            title='Connect to GrantaMI Database',
        )

        return view

    def can_connect(self):
        """Test connection to database and display a dialog message if
        any errors are raised

        Returns
        -------
        bool
            True if connection is sucessful
        """
        can_connect, conn_or_error = self.model.test_connection()
        if not can_connect:
            dlg = MessageDialog()
            dlg.error(str(conn_or_error))

        return can_connect

    def close(self, info, is_ok):
        """Test connection to database upon closure of UI."""

        # Don't perform any actions if the user clicks "Cancel"
        if not is_ok:
            return True

        return self.can_connect()
