from typing import List, Dict

from bible_maker.bible_objects import Bible, Book, Chapter, CarriageReturn, Verse


def dataset_to_ints(dataset: Dict[str, Dict[str, List[List[int]]]]) -> Dict[str, Dict[int, List[List[int]]]]:
    """The current implementation of the paragrapher uses strings instead of integers"""
    return {book_name: {int(chapter_idx): verses for chapter_idx, verses in chapters.items()} for book_name, chapters in dataset.items()}


def update_chapter(chapter: Chapter, dataset: List[List[int]]):
    """Adds the CarriageReturns at the end of each list"""
    for paragraph in dataset:
        for idx, verse in enumerate(chapter.verses):
            if isinstance(verse, Verse) and paragraph[-1] == verse.num:
                chapter.verses.insert(idx + 1, CarriageReturn())
                break


def update_book(book: Book, dataset: Dict[int, List[List[int]]]):
    """Simple iterator for books"""
    for chapter in book.chapters:
        if chapter.num in dataset:
            update_chapter(chapter, dataset[chapter.num])


def update_bible(bible: Bible, dataset: Dict[str, Dict[str, List[List[int]]]]):
    """Adds carriage returns to a bible"""
    dataset = dataset_to_ints(dataset)
    for book in bible.ot_books + bible.nt_books:
        if book.name in dataset:
            update_book(book, dataset[book.name])
