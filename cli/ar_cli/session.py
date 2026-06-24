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

"""Build invocation request headers, including the session headers.

Kept separate so future `resume` / `fork` commands can reuse the same header
construction logic.
"""

import json
from typing import Dict, Optional

from ar_cli.const import (
    ACCEPT_SSE,
    CONTENT_TYPE_JSON,
    DEFAULT_CONCURRENCY,
    DEFAULT_SESSION_TTL,
    HEADER_ACCEPT,
    HEADER_AGENT_SESSION,
    HEADER_CONTENT_TYPE,
    HEADER_INSTANCE_SESSION,
)


def build_invocation_headers(
    session_ctx: Optional[str] = None,
    session_id: Optional[str] = None,
    session_ttl: Optional[int] = None,
    concurrency: Optional[int] = None,
) -> Dict[str, str]:
    """Construct headers for a function invocation.

    ``Content-Type`` and ``Accept`` are always present. The session headers are
    conditional:

    - ``X-Agent-Session`` only when ``session_ctx`` is given.
    - ``X-Instance-Session`` only when ``session_id`` is given; ``session_ttl``
      and ``concurrency`` fall back to their defaults (90 / 1) when ``None``.
    """
    headers: Dict[str, str] = {
        HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
        HEADER_ACCEPT: ACCEPT_SSE,
    }

    if session_ctx is not None:
        headers[HEADER_AGENT_SESSION] = json.dumps({"sessionCtx": session_ctx})

    if session_id is not None:
        ttl = session_ttl if session_ttl is not None else DEFAULT_SESSION_TTL
        conc = concurrency if concurrency is not None else DEFAULT_CONCURRENCY
        headers[HEADER_INSTANCE_SESSION] = json.dumps(
            {"sessionID": session_id, "sessionTTL": ttl, "concurrency": conc}
        )

    return headers
