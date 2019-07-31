#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyatlonajuno` package."""

import pytest
from unittest.mock import MagicMock, Mock

from click.testing import CliRunner

from pyatlonajuno import lib
from pyatlonajuno import cli


@pytest.fixture
def j451():
    j = lib.Juno451("url")
    j.requests = MagicMock()
    j.requests.get = MagicMock()
    return j


def test_getPowerState(j451):
    j451.getPowerState()
    j451.requests.get.assert_called_with('url/aj.html?a=sys')


def test_setPowerState(j451):
    j451.setPowerState("on")
    j451.requests.get.assert_called_with('url/aj.html?a=command&cmd=PWON')


def test_getSource(j451):
    j451.getSource()
    j451.requests.get.assert_called_with('url/aj.html?a=avs')


def test_setSource(j451):
    j451.setSource(1)
    j451.requests.get.assert_called_with('url/aj.html?a=command&cmd=x1AVx1')


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    #assert 'pyatlonajuno.cli.main' in result.output
    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
