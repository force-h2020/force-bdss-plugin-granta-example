#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Any

from force_bdss.api import (
    BaseDataSourceModel,
    BaseNotificationListener, BaseNotificationListenerModel)

from .granta_mixin_classes import GrantaAuthMixin, create_session


class BaseGrantaDataSourceModel(GrantaAuthMixin, BaseDataSourceModel):
    """A BaseDataSourceModel with traits containing
    Granta MI authentication details"""


class BaseGrantaNotificationListener(BaseNotificationListener):
    """A BaseNotificationListener with utility traits and methods for
    connecting to a Granta MI database"""

    #: Reference to the GrantaMI session
    _mi = Any()

    def initialize(self, model):
        """Initializes a session with a Granta MI database

        Parameters
        ----------
        model: BaseGrantaNotificationListenerModel
            Model associated with this class
        """
        self._mi = create_session(model)


class BaseGrantaNotificationListenerModel(
        GrantaAuthMixin, BaseNotificationListenerModel):
    """A BaseNotificationListenerModel with traits containing
    Granta MI authentication details"""
