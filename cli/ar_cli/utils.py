#!/usr/bin/env python3
# coding=UTF-8
# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging setup and small helpers shared across commands."""

import json
import logging
import os
import re
import sys
from typing import Any

import click

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

# Diagnostic logger -> stderr. The ar CLI never writes log files: it is a
# short-lived, stateless HTTP client. Users who want logs on disk redirect
# stderr (e.g. `ar exec ... 2> ar.log`).
_LOG_FORMAT = "%(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Clean output logger -> stdout. Carries command results and the streamed SSE
# payloads, with no prefixes, so piping/redirecting stays clean.
print_logger = logging.getLogger("ar.print")
print_logger.setLevel(logging.INFO)
print_logger.propagate = False
_print_handler = logging.StreamHandler(sys.stdout)
_print_handler.setFormatter(logging.Formatter("%(message)s"))
print_logger.addHandler(_print_handler)


def setup_logging(verbose: bool) -> None:
    """Configure root logging to the console (stderr).

    DEBUG when ``verbose`` is set (shows request details), otherwise INFO.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=_LOG_FORMAT,
        datefmt=_DATE_FORMAT,
        force=True,
    )


def normalize_addr(addr: str) -> str:
    """Normalize a user-supplied address to a URL base.

    Users pass a bare ``host:port`` (no scheme); http is assumed and prepended.
    An address that already carries a scheme is left as-is.
    """
    addr = addr.strip()
    if not _SCHEME_RE.match(addr):
        addr = "http://" + addr
    return addr


def load_spec(spec_arg: str) -> Any:
    """Load a function spec from an inline JSON string or a JSON file path.

    A value that points to an existing file is read from disk; anything else is
    parsed as an inline JSON string. Invalid input raises ``click.BadParameter``
    so the process exits with the standard parameter-error code (2).
    """
    raw = spec_arg
    if os.path.isfile(spec_arg):
        try:
            with open(spec_arg, "r", encoding="utf-8") as f:
                raw = f.read()
        except OSError as e:
            raise click.BadParameter(f"failed to read spec file '{spec_arg}': {e}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        hint = spec_arg if os.path.isfile(spec_arg) else _truncate(raw)
        raise click.BadParameter(f"spec is not valid JSON ({hint}): {e}")


def parse_json_arg(value: str, label: str) -> Any:
    """Validate that ``value`` is a JSON document, raising ``BadParameter`` if not."""
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise click.BadParameter(f"{label} is not valid JSON ({_truncate(value)}): {e}")


def _truncate(text: str, limit: int = 120) -> str:
    text = text.strip().replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + "..."
