#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import granta

from traits.api import HasStrictTraits, Str, Password


class GrantaAuthMixin(HasStrictTraits):
    """Mixin class containing traits required for authentication
    to a Granta MI database
    """

    #: URL of Granta database, by default the FORCE database is provided
    url = Str('https://force.granta.com/mi_servicelayer/')

    #: Login name, must be provided by the user
    login = Str()

    #: Login password, must be provided by the user
    password = Password()

    #: Optional domain of database connection
    domain = Str()

    #: Reference key to FORCE Granta database
    db_key = Str('MI_Force')


def create_session(model):
    """Sets up a Granta MI database session using authentication
    details in model

    Parameters
    ----------
    model: GrantaAuthMixin
        Object that inherits from GrantaAuthMixin and thereby
        provides access information to a database
    """
    return granta.connect(
        model.url,
        user_name=model.login,
        password=model.password,
        domain=model.domain
    )
