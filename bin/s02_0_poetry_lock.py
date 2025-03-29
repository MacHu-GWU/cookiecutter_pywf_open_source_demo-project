#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyproject_ops.cli import pyops

pyops.poetry_lock(real_run=True, verbose=True)
