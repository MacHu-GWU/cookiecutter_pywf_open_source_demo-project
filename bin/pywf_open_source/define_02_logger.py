# -*- coding: utf-8 -*-

"""
Logging related automation.
"""

import typing as T
import dataclasses

from .logger import logger
from .vendor.emoji import Emoji

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfLogger:
    """
    Namespace class for Virtualenv management related automation.

    :param python_version: example "3.7", "3.8", ...
    """

    def _with_logger(
        self: "PyWf",
        method,
        msg: str,
        emoji: str,
        verbose: bool = False,
        **kwargs,
    ):
        """
        A helper method to wrap a regular method with logger
        """
        if verbose:

            @logger.start_and_end(
                msg=msg,
                start_emoji=emoji,
                error_emoji=f"{Emoji.failed} {emoji}",
                end_emoji=f"{Emoji.succeeded} {emoji}",
                pipe=emoji,
            )
            def func():
                return method(**kwargs)

            return func()
        else:
            return method(**kwargs)
