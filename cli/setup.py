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

"""Packaging for the openYuanrong Agent Runtime CLI (`ar`)."""

import os
import re

import setuptools

ROOT_DIR = os.path.dirname(__file__)


def get_version():
    """Read __version__ from ar_cli/__init__.py."""
    init_path = os.path.join(ROOT_DIR, "ar_cli", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if not match:
        raise RuntimeError("Unable to find __version__ in ar_cli/__init__.py")
    return os.getenv("BUILD_VERSION") or match.group(1)


setuptools.setup(
    name="openyuanrong-agentruntime",
    version=get_version(),
    author="openyuanrong",
    description="openYuanrong Agent Runtime CLI (ar): deploy and invoke agents",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.9",
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        "click>=8.1",
        "requests>=2.28",
    ],
    entry_points={
        "console_scripts": [
            "ar=ar_cli.main:main",
        ]
    },
)
