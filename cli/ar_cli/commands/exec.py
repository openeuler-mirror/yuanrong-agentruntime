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

"""`ar exec` — invoke an agent (function) and stream the SSE response."""

import logging

import click

from ar_cli.client import AgentRuntimeClient
from ar_cli.errors import ArError
from ar_cli.session import build_invocation_headers
from ar_cli.sse import stream_sse
from ar_cli.utils import normalize_addr, parse_json_arg, print_logger

logger = logging.getLogger(__name__)


@click.command(
    name="exec",
    help="""Invoke an agent (function) and stream its SSE response.

Only --agent and --server are required. Session headers are sent only when their
options are provided: --session-ctx adds X-Agent-Session, --session-id adds
X-Instance-Session (with --session-ttl / --concurrency, defaults 90 / 1).

Example:\n
  ar exec --agent <URN> --server <FRONTEND_ADDR> --args '{"param1":"hi"}'
""",
)
@click.option("--agent", required=True, help="functionVersionUrn of the agent to invoke.")
@click.option(
    "--server",
    required=True,
    help="frontend address as host:port, e.g. 127.0.0.1:31180 (http is assumed, no scheme needed).",
)
@click.option("--session-ctx", default=None, help="Agent session context; sets the X-Agent-Session header.")
@click.option("--session-id", default=None, help="Instance session id; sets the X-Instance-Session header.")
@click.option(
    "--session-ttl",
    type=int,
    default=None,
    help="Instance session TTL (default: 90). Only used with --session-id.",
)
@click.option(
    "--concurrency",
    type=int,
    default=None,
    help="Instance session concurrency (default: 1). Only used with --session-id.",
)
@click.option("--args", "args", default=None, help="Handler arguments as a JSON string. Omit to send no body.")
@click.pass_context
def exec_cmd(
    ctx: click.Context,
    agent: str,
    server: str,
    session_ctx: str,
    session_id: str,
    session_ttl: int,
    concurrency: int,
    args: str,
) -> None:
    # session-ttl / concurrency are meaningless without a session id.
    if session_id is None and (session_ttl is not None or concurrency is not None):
        logger.warning("--session-ttl/--concurrency are ignored without --session-id")

    body = None
    if args is not None:
        parse_json_arg(args, "--args")  # validate early; exit code 2 on bad JSON
        body = args

    headers = build_invocation_headers(
        session_ctx=session_ctx,
        session_id=session_id,
        session_ttl=session_ttl,
        concurrency=concurrency,
    )

    client = AgentRuntimeClient()
    try:
        resp = client.invoke(normalize_addr(server), agent, headers=headers, body=body)
        with resp:
            for payload in stream_sse(resp):
                print_logger.info("%s", payload)
    except ArError as e:
        logger.error("%s", e)
        ctx.exit(e.exit_code)
    ctx.exit(0)
