# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Test Invenio Assets module."""

from __future__ import absolute_import, print_function

from os.path import exists, isfile, join
from time import sleep

from click.testing import CliRunner
from flask_assets import assets

from invenio_assets.cli import collect


def test_invenio_assets_assets(app, script_info_assets, testcss):
    """Test assets command in assets CLI."""
    static_root = app.extensions['collect'].static_root
    cache_dir = join(static_root, '.webassets-cache')
    css_path = join(static_root, 'test.css')
    bundle_path = join(static_root, 'testbundle.css')

    # Run collect
    runner = CliRunner()
    assert not exists(css_path)
    result = runner.invoke(collect, [], obj=script_info_assets)
    assert result.exit_code == 0 and isfile(css_path)

    # Run build
    assert not exists(bundle_path)
    result = runner.invoke(assets, ['build'], obj=script_info_assets)
    assert result.exit_code == 0 and isfile(bundle_path)
    assert exists(cache_dir)

    # Clean cache
    result = runner.invoke(assets, ['clean'], obj=script_info_assets)
    assert result.exit_code == 0 and not exists(cache_dir)


def test_collect(app, script_info_assets, testcss):
    """Test assets command in assets CLI."""
    css_path = join(app.extensions['collect'].static_root, 'test.css')

    # Run collect
    runner = CliRunner()
    assert not exists(css_path)
    result = runner.invoke(collect, ['-v'], obj=script_info_assets)
    assert result.exit_code == 0
    assert "Copied: [conftest] '{0}'".format(css_path) in result.output

    # Run collect again - no file copied
    result = runner.invoke(collect, ['-v'], obj=script_info_assets)
    assert result.exit_code == 0
    assert 'Copied' not in result.output

    # Modify file (and ensure timestamp is different)
    sleep(1)
    with open(testcss, 'w') as fp:
        fp.write('* {color: black;}')

    # Run collect again - file will be copied
    result = runner.invoke(collect, ['-v'], obj=script_info_assets)
    assert result.exit_code == 0
    assert 'Copied' in result.output
