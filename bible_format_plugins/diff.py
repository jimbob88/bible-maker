import itertools
import re
from collections import OrderedDict
from typing import Sequence, List, Tuple, NamedTuple

from bible_maker.bible_objects import Verse, Chapter, Book, Bible
from bible_maker.conversion_table import joined_conversion_table, conversion_table


def verse_regex(abbreviations: Sequence[str]):
    """Generates a regex that matches all lines in a diff file

    :param abbreviations:  A list of abbreviations like ["PSA", "GLO", "FRT"]
    :return: A regex that matches diff lines
    """
    return r"(" + '|'.join(abbreviations) + r") (\d+):(\d+) (.*)"


def group_bible_by_book(bible: str, regex: str) -> OrderedDict[str, List[Tuple[str, str, str, str]]]:
    """

    :param bible: The text of the bible ( a diff text )
    :param regex: The regex which matches [GEN 1:1 TEXT]
    :return: {'GEN': [('GEN', '1', '1', 'TEXT')]}
    """
    versed = re.findall(regex, bible, re.MULTILINE)
    return OrderedDict([(item[0], list(item[1])) for item in itertools.groupby(versed, key=lambda x: x[0])])


def separate_by_chapter(verses: List[Tuple[str, str, str, str]]) -> OrderedDict[int, List[Tuple[str, str, str, str]]]:
    """Given a list of the verses in a book, separates them by chapter number"""
    return OrderedDict((int(item[0]), list(item[1])) for item in itertools.groupby(verses, key=lambda x: x[1]))


def verse(v: Tuple[str, str, str, str]) -> Verse:
    """Converts the `diff` format to a python verse object"""
    return Verse(
        num=int(v[2]),
        text=v[3]
    )


def chapter(chapter_num: int, chap_verses: List[Tuple[str, str, str, str]]) -> Chapter:
    """Converts the `diff` format to a python chapter object"""
    return Chapter(
        num=chapter_num,
        verses=[verse(v) for v in chap_verses]
    )


def book(book_name: str, verses: List[Tuple[str, str, str, str]]):
    """Converts the `diff` format to a python book object"""
    return Book(
        book_name,
        [chapter(chapter_num, chap_verses) for chapter_num, chap_verses in separate_by_chapter(verses).items()]
    )


class BookCollection(NamedTuple):
    """A simple return type which separates the old and new testaments"""
    ot_books: List[Book]
    nt_books: List[Book]


def versed_books_to_testaments(versed_book: OrderedDict[str, list[tuple[str, str, str, str]]]) -> BookCollection:
    """Converts the Grouped Bible Format to two lists of the testament books"""
    ot_books = []
    nt_books = []

    for abbreviated_name, verses in versed_book.items():
        book_name = joined_conversion_table[abbreviated_name]
        bk = book(book_name, verses)
        if abbreviated_name in conversion_table['ot']:
            ot_books.append(bk)
        else:
            nt_books.append(bk)
    return BookCollection(ot_books, nt_books)


def diff_to_bible(diff_source: str):
    """Converts a diff file to a bible python object"""
    v_regex = verse_regex(joined_conversion_table)
    versed_books = group_bible_by_book(diff_source, v_regex)
    testaments = versed_books_to_testaments(versed_books)

    return Bible(
        testaments.ot_books, testaments.nt_books
    )
