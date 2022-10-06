# -*- coding: UTF-8 -*-
"""
Created on 06.10.22

:author:     Martin Dočekal
"""
import json
from io import StringIO
from unittest import TestCase

from fileindexer.__main__ import index_file


class TestIndexFile(TestCase):
    def setUp(self) -> None:
        self.file_content = [
            {"k": 1, "other": "content 1"},
            {"k": 0, "other": "content 2"},
            {"k": 10, "other": "content 3"},
            {"k": 20, "other": "content 4"},
            {"k": 40, "other": "content 5"},
            {"k": 60, "other": "content 6"},
        ]
        self.offsets = []
        self.file_content = ""
        self.plain_index_content = ""
        self.key_index_content = ""
        for c in self.file_content:
            act_line = json.dumps(c) + "\r\n"
            self.offsets.append(len(act_line))
            self.file_content += act_line
            self.plain_index_content += f"{act_line}\r\n"
            self.key_index_content += f"{c['k']}\t{act_line}\r\n"

        self.file = StringIO(self.file_content)
        self.index = StringIO()

    def test_base_conf(self):
        self.assertEqual(len(self.file_content), index_file(self.file, self.index))
        self.assertEqual(self.plain_index_content, self.index.getvalue())

    def test_with_key(self):
        self.assertEqual(len(self.file_content), index_file(self.file, self.index, key="k"))
        self.assertEqual(self.key_index_content, self.index.getvalue())

    def test_headline_unk_names(self):
        with self.assertRaises(AssertionError):
            index_file(self.file, self.index, True)

    def test_headline_unk_name_for_key(self):
        with self.assertRaises(AssertionError):
            index_file(self.file, self.index, True, key="k", name_offset="file_line_offset")

    def test_headline_without_key(self):
        self.assertEqual(len(self.file_content), index_file(self.file, self.index, True,
                                                            name_offset="file_line_offset"))
        headline, rest = self.index.getvalue().split("\r\n", maxsplit=1)
        self.assertEqual("file_line_offset", headline)
        self.assertEqual(self.plain_index_content, rest)

    def test_headline_with_key(self):
        index_file(self.file, self.index, True, key="k", name_key="key", name_offset="file_line_offset")
        headline, rest = self.index.getvalue().split("\r\n", maxsplit=1)
        self.assertEqual("key\tfile_line_offset", headline)
        self.assertEqual(self.key_index_content, rest)
