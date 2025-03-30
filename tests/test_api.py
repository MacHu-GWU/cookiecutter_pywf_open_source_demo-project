# -*- coding: utf-8 -*-

from cookiecutter_pywf_open_source_demo import api


def test():
    _ = api


if __name__ == "__main__":
    from cookiecutter_pywf_open_source_demo.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_pywf_open_source_demo.api",
        preview=False,
    )
