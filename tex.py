from typing import Union, Iterator

from bible_maker.bible_objects import Verse, CarriageReturn, Chapter, Book, Bible


def tex_title(title: str) -> str:
    """Initiates a new Book (as a LaTeX chapter)"""
    return (
            r'\chapter{%s}\pagebreak[1]'
            '\n'
            r'\begin{multicols}{2}'
            '\n' % title
    )


def verse_to_tex(verse: Union[Verse, CarriageReturn]) -> str:
    """Given a verse returns the tex verse number + string

    This also adds carriage returns for the paragrapher.
    """
    if isinstance(verse, Verse):
        return (
                '$^{%s}$ %s\n'
                % (verse.num, verse.text)
        )
    if isinstance(verse, CarriageReturn):
        return "\n"
    raise NotImplementedError(f"Couldn't deal with {verse}!")


def chapter_to_tex(chapter: Chapter) -> str:
    """Creates a chapter subheading and then adds all the verses afterwards"""
    chap_text = (
            r'\subparagraph*{%s}'
            '\n'
            % chapter.num
    )
    chap_text += ''.join(verse_to_tex(verse) for verse in chapter.verses)

    return chap_text


def testament_to_tex(testament: Iterator[Book]) -> str:
    """Given a list of books convert to tex equivalent"""
    testament_text = ""
    for book in testament:
        testament_text += tex_title(book.name)
        testament_text += ''.join(chapter_to_tex(chapter) for chapter in book.chapters)
        testament_text += "\\end{multicols}"
    return testament_text


def bible_to_tex(bible: Bible) -> str:
    """Adds the Old and New testament in tex"""
    text = "\\part{Old Testament}\n"
    text += testament_to_tex(bible.ot_books)
    text += "\n\\part{New Testament}\n"
    text += testament_to_tex(bible.nt_books)

    return text
