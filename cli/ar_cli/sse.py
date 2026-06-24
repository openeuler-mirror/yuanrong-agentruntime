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

"""Streaming Server-Sent Events (SSE) parser.

Shared by every invocation-style command (exec, and future resume/fork) so they
print server data incrementally as it arrives.
"""

from typing import Iterator

from ar_cli.const import SSE_DATA_PREFIX, SSE_DONE_MARKER


def stream_sse(response) -> Iterator[str]:
    """Yield ``data:`` payloads from an SSE response, one event at a time.

    Blank lines separating events are skipped. Iteration stops at the
    ``data: [DONE]`` terminator. Heartbeat frames such as ``data: {}`` are
    passed through unchanged so the caller can decide what to do with them.
    """
    for raw in response.iter_lines(decode_unicode=True):
        if not raw:
            # Event separator (blank line) or keep-alive newline.
            continue
        if raw.startswith(SSE_DATA_PREFIX):
            payload = raw[len(SSE_DATA_PREFIX):].strip()
            if payload == SSE_DONE_MARKER:
                return
            yield payload
