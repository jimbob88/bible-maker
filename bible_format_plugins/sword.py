from typing import List, Generator

from pysword.bible import SwordBible
from pysword.books import BookStructure

from bible_maker.bible_objects import Verse, Chapter, Book, Bible


def testament_books(books: List[BookStructure], bible: SwordBible) -> Generator[Book, None, None]:
    for book in books:
        chapters = []
        for chapter_num in range(book.num_chapters):
            verses = [Verse(verse_num + 1, bible.get(books=[book.name], chapters=[book.chapter_offset(chapter_num)], verses=[verse_num]))
                      for verse_num in range(1, book.chapter_lengths[chapter_num])]
            chapters.append(Chapter(chapter_num + 1, verses))
        yield Book(book.name, chapters)


def sword_bible_to_bible(bible: SwordBible) -> Bible:
    books = bible.get_structure().get_books()
    ot = list(testament_books(books['ot'], bible))
    nt = list(testament_books(books['nt'], bible))
    return Bible(ot_books=ot, nt_books=nt)
