# -*- coding: utf-8 -*-

from cookiecutter_pywf_open_source_demo.example_module_1 import add_two


def test_add_two():
    assert add_two(1, 2) == 3


if __name__ == "__main__":
    from cookiecutter_pywf_open_source_demo.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_pywf_open_source_demo.example_module_1",
        preview=False,
    )
