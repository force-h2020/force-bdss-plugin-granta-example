#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import HasStrictTraits, Instance, Any

from granta_example.core.granta_mixin_classes import create_session

from .granta_login_view import GrantaLoginModel


class GrantaSessionManager(HasStrictTraits):

    # Current active GrantaMI session
    session = Any()

    # Model object holding login and connection details
    login_model = Instance(GrantaLoginModel)

    def update_session(self):
        self.session = create_session(self.login_model)


def create_session_manager():
    model = GrantaLoginModel()
    return GrantaSessionManager(login_model=model)
