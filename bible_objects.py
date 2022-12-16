import dataclasses
from typing import NamedTuple, List, Union


class Verse(NamedTuple):
    num: int
    text: str


class CarriageReturn(NamedTuple):
    ...


class Chapter(NamedTuple):
    num: int
    verses: List[Union[Verse, CarriageReturn]]


class Book(NamedTuple):
    name: str
    chapters: List[Chapter]


@dataclasses.dataclass
class Bible:
    ot_books: List[Book]
    nt_books: List[Book]
    name: str = ''
    author: str = ''
    copyright_notice: str = ''
