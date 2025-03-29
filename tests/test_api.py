# -*- coding: utf-8 -*-

from cookiecutter_pyproject_demo import api


def test():
    _ = api


if __name__ == "__main__":
    from cookiecutter_pyproject_demo.tests import run_cov_test

    run_cov_test(__file__, "cookiecutter_pyproject_demo.api", preview=False)
