# !/usr/bin/python
# -*- coding: UTF-8 -*-

import pathlib

import aiosql



record = {}
queries = aiosql.from_path(pathlib.Path(__file__).parent / "sql", "pymysql", record_classes=record)
