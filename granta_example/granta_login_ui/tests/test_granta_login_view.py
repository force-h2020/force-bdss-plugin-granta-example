#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from granta_example.granta_login_ui.granta_login_view import (
    GrantaLoginModel, GrantaLoginView)


class TestGrantaLoginView(TestCase):

    def setUp(self):
        self.model = GrantaLoginModel()
        self.view = GrantaLoginView(model=self.model)
