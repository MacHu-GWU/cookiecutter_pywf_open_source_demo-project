#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyproject_ops.cli import pyops

pyops.poetry_install_only_root(real_run=True, verbose=True)
