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

from ar_cli.utils import normalize_addr


def test_bare_host_port_gets_http():
    assert normalize_addr("127.0.0.1:31182") == "http://127.0.0.1:31182"


def test_existing_http_scheme_kept():
    assert normalize_addr("http://127.0.0.1:31182") == "http://127.0.0.1:31182"


def test_existing_https_scheme_kept():
    assert normalize_addr("https://host:443") == "https://host:443"


def test_surrounding_whitespace_stripped():
    assert normalize_addr("  host:8080  ") == "http://host:8080"
