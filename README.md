# FileIndexer
Tool for creating line offset indexes as tsv files.

# Install

You can download this repository or directly install with:

    pip install fileindexer

# Index format
The index in basic case is formated as one column tsv file with voluntary headline containing file line offset.

This indexer also supports to create key mapping to given file line offset if jsonl file is provided. In that case the 
index is two column tsv file with first column containing key and second the corresponding file offset.

Feel free to visit <i>examples</i> folder with toy example to get more familiar with the format.

# Examples
This repository contains <i>examples</i> folder with variants of indexes that could be created. Bellow follows list of
commands that were used for creating those indexes:

* toy_basic.jsonl.index


    fileindexer examples/toy.jsonl examples/toy_basic.jsonl.index

* toy_basic_with_headline.jsonl.index


    fileindexer examples/toy.jsonl examples/toy_basic_with_headline.jsonl.index --headline --name_offset "file_line_offset"

* toy_key_mapping.jsonl.index


    fileindexer examples/toy.jsonl examples/toy_key_mapping.jsonl.index --key k

* toy_key_mapping_with_headline.jsonl.index


    fileindexer examples/toy.jsonl examples/toy_key_mapping_with_headline.jsonl.index --key k --headline --name_key key --name_offset "file_line_offset"