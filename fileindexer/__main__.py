# -*- coding: UTF-8 -*-
"""
Created on 06.10.22
Wrapper for running fileindexer directly.

:author:     Martin Dočekal
"""
import csv
import io
import json
import logging
import random
import sys
import time
from argparse import ArgumentParser
from typing import TextIO, Optional

from tqdm import tqdm


class ArgumentParserError(Exception):
    """
    Exceptions for argument parsing.
    """
    pass


class ExceptionsArgumentParser(ArgumentParser):
    """
    Argument parser that uses exceptions for error handling.
    """

    def error(self, message):
        raise ArgumentParserError(message)


class ArgumentsManager(object):
    """
    Parsers arguments for script.
    """

    @classmethod
    def parseArgs(cls):
        """
        Performs arguments parsing.

        :param cls: arguments class
        :returns: Parsed arguments.
        """

        parser = ExceptionsArgumentParser(
            description="Script for indexing text files using line offsets.")

        parser.add_argument("file", help="Text file for indexing.", type=str)
        parser.add_argument("index", help="Path to index file that should be created.", type=str)
        parser.add_argument("--headline", help="Creates headline in index file with field names, "
                                               "see name* attributes.", action="store_true")
        parser.add_argument("--key", help="Allows to create mapping from key to line offsets. If the key attribute is"
                                          "used it is expected that the original file is in jsonl format and this"
                                          "attribute states name of field that should be used for key mapping.",
                            type=str)
        parser.add_argument("--name_key", help="Name for key field in index.", type=str)
        parser.add_argument("--name_offset", help="Name for line offset field in index.", type=str)

        if len(sys.argv) < 2:
            parser.print_help()
            return None
        try:
            parsed = parser.parse_args()

        except ArgumentParserError as e:
            parser.print_help()
            print("\n" + str(e), file=sys.stdout, flush=True)
            return None

        return parsed


def index_file(file: TextIO, ind: TextIO, headline: bool = False, key: Optional[str] = None,
               name_offset: Optional[str] = None, name_key: Optional[str] = None):
    """
    Creates line offset index, in form of tsv file, for given file.

    :param file: Text file for indexing.
    :param ind: file for writing the index
    :param headline: Creates headline in index file with field names, see name* attributes.
    :param key: Allows to create mapping from key to line offsets. If the key attribute is used it is expected that
        the original file is in jsonl format and this attribute states name of field that should be used for key mapping.
    :param name_offset: Name for key field in index.
    :param name_key: Name for line offset field in index.
    :return: number of indexed lines
    """

    writer = csv.writer(ind, delimiter="\t", quotechar='|')
    if headline:
        assert (name_offset is not None) and \
               (key is None or name_key is not None), \
            "When headline should be printed, you must provide all field names."
        writer.writerow([name_offset] if key is None else [name_key, name_offset])

    file.seek(0, io.SEEK_END)
    file_size = file.tell()
    with tqdm(desc="indexing", total=file_size, unit="bytes") as p_bar:
        file.seek(0)
        previous, line_cnt = 0, 0
        while line := file.readline():
            writer.writerow([previous] if key is None else [json.loads(line)[key], previous])
            p_bar.update(file.tell() - previous)
            previous = file.tell()
            line_cnt += 1
    return line_cnt


def main():
    args = ArgumentsManager.parseArgs()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    if args is not None:
        with open(args.file, "r") as f, open(args.index, "w") as ind:
            logging.info("start of indexing")
            line_cnt = index_file(f, ind, args.headline, args.key, args.name_offset, args.name_key)
            logging.info(f"{line_cnt}\tlines indexed")
            logging.info("finished")
    else:
        exit(1)


if __name__ == '__main__':
    main()
