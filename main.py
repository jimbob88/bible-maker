import argparse
import contextlib
import itertools
import json
import re
from collections import OrderedDict
from pathlib import Path
from string import Template
from typing import Sequence, Tuple, List

from pysword.modules import SwordModules

from conversion_table import joined_conversion_table


class MyTemplate(Template):
    """A template for `.tex` files

    https://stackabuse.com/formatting-strings-with-the-python-template-class/
    """
    delimiter = '$'


def get_args():
    parser = argparse.ArgumentParser(description="A software for generating bibles")
    parser.add_argument('--module', '-m', required=False, help="Choose which bible SWORD module zip to use")
    parser.add_argument('--bibletxt', '-b', required=False, help="Choose which bible DIFFABLE you will use")
    parser.add_argument('--paragrapher', '-p', required=False, help="select where the paragraphing json is")
    return parser.parse_args()


def load_json(file: str):
    return json.load(Path(file).open('r', encoding='utf-8'))


def verse_regex(abbreviations: Sequence[str]):
    return r"(" + '|'.join(abbreviations) + r") (\d+):(\d+) (.*)"


def group_bible_by_book(bible: str, regex: str) -> OrderedDict[str, List[Tuple[str, str, str, str]]]:
    """

    :param bible: The text of the bible ( a diff text )
    :param regex: The regex which matches [GEN 1:1 TEXT]
    :return: {'GEN': [('GEN', '1', '1', 'TEXT')]}
    """
    versed = re.findall(regex, bible, re.MULTILINE)
    return OrderedDict([(item[0], list(item[1])) for item in itertools.groupby(versed, key=lambda x: x[0])])


def tex_title(title: str) -> str:
    return (
            r'\part{%s}\pagebreak[1]'
            '\n'
            r'\begin{multicols}{2}'
            '\n' % title
    )


def chapters(verses: List[Tuple[str, str, str, str]]) -> OrderedDict[int, List[Tuple[str, str, str, str]]]:
    """Given a list of the verses in a book, separates them by chapter number"""
    return OrderedDict((int(item[0]), list(item[1])) for item in itertools.groupby(verses, key=lambda x: x[1]))


def diff_main(args):
    if args.paragrapher is not None:
        para = load_json(args.paragrapher)

    v_regex = verse_regex(joined_conversion_table)

    bible = Path(args.bibletxt).read_text(encoding='utf-8')
    versed_book = group_bible_by_book(bible, v_regex)

    text = ""
    for abbreviated_name, verses in versed_book.items():
        book_name = joined_conversion_table[abbreviated_name]
        text += tex_title(book_name)

        for chapter_num, chap_verses in chapters(verses).items():
            text += (
                    r'\subparagraph*{%s}'
                    '\n'
                    % chapter_num
            )
            for verse in chap_verses:
                _, _, verse_num, verse_string = verse
                text += (
                        '$^{%s}$ %s\n'
                        % (verse_num, verse_string)
                )
                if args.paragrapher is not None:
                    with contextlib.suppress(KeyError):
                        for paragraph in para[book_name][f"{chapter_num:02d}"]:
                            if int(verse_num) == paragraph[-1]:
                                text += r'\par'

        text += (
            r'\end{multicols}'
            '\n'
        )
    return text


def pysword_main(args):
    if args.paragrapher is not None:
        para = load_json(args.paragrapher)
    modules = SwordModules(args.module)
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module(Path(args.module).stem)

    text = ""
    for testament, books in bible.get_structure().get_books().items():
        for book in books:
            text += tex_title(book.name)
            for chapter_num in range(book.num_chapters):
                print(f'{book.name} - {chapter_num}')
                text += (
                        r'\subparagraph*{%s}'
                        '\n'
                        % (chapter_num + 1)
                )
                for verse_num in range(1, book.chapter_lengths[chapter_num]):
                    verse = bible.get(books=[book.name], chapters=[chapter_num + 1], verses=[verse_num])
                    text += (
                            '$^{%s}$ %s\n'
                            % (verse_num, verse)
                    )
                    if args.paragrapher is not None:
                        with contextlib.suppress(KeyError):
                            for paragraph in para[book.name][f"{chapter_num:02d}"]:
                                if int(verse_num) == paragraph[-1]:
                                    text += r'\par'
    text += (
        r'\end{multicols}'
        '\n'
    )
    return text


if __name__ == '__main__':
    args = get_args()
    if args.bibletxt:
        text = diff_main(args)
    elif args.module:
        text = pysword_main(args)
    else:
        text = ""

    template = MyTemplate(Path('template.tex').read_text(encoding='utf-8'))
    Path('generate.tex').write_text(template.substitute(books=text), encoding='utf-8')
