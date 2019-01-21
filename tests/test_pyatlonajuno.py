#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyatlonajuno` package."""

import pytest
from unittest.mock import MagicMock, Mock

from click.testing import CliRunner

from pyatlonajuno import lib
from pyatlonajuno import cli

LOGIN_SIDE_EFFECT = ['Login Please Username :',
                     'Password :',
                     'Welcome to TELNET']


@pytest.fixture
def j451():
    j = lib.Juno451("user", "pass", "host")
    j.conn = MagicMock()
    j.conn.read_until = MagicMock()
    j.conn.read_until.side_effect = LOGIN_SIDE_EFFECT
    return j


def test_login(j451):
    j451.login()


def test_getPowerState(j451):
    j451.conn.read_until.side_effect = LOGIN_SIDE_EFFECT + ["PWSTA", "PWOFF"]
    assert j451.getPowerState() == "off"


def test_setPowerState(j451):
    j451.conn.read_until.side_effect = LOGIN_SIDE_EFFECT + ["PWON", "PWON"]
    assert j451.setPowerState("on") == "PWON"


def test_getInputState(j451):
    j451.conn.read_until.side_effect = (LOGIN_SIDE_EFFECT +
                                        ["InputStatus",
                                         "InputStatus 1000"])
    assert j451.getInputState() == [True, False, False, False]


def test_getSource(j451):
    j451.conn.read_until.side_effect = (LOGIN_SIDE_EFFECT +
                                        ["Status",
                                         "x1AVx1"])
    assert j451.getSource() == 1


def test_setSource(j451):
    j451.conn.read_until.side_effect = (LOGIN_SIDE_EFFECT +
                                        ["x1AVx1",
                                         "x1AVx1"])
    assert j451.setSource(1) == 1


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    #assert 'pyatlonajuno.cli.main' in result.output
    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
