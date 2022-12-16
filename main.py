import argparse
import json
from pathlib import Path
from string import Template
from typing import Iterator, Union

from pysword.modules import SwordModules

from bible_maker.bible_format_plugins.diff import diff_to_bible
from bible_maker.bible_format_plugins.sword import sword_bible_to_bible
from bible_maker.bible_objects import Bible, Book, Chapter, Verse, CarriageReturn


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


def tex_title(title: str) -> str:
    return (
            r'\chapter{%s}\pagebreak[1]'
            '\n'
            r'\begin{multicols}{2}'
            '\n' % title
    )


def verse_to_tex(verse: Union[Verse, CarriageReturn]) -> str:
    if isinstance(verse, Verse):
        return (
                '$^{%s}$ %s\n'
                % (verse.num, verse.text)
        )
    if isinstance(verse, CarriageReturn):
        return "\n"
    raise NotImplementedError(f"Couldn't deal with {verse}!")


def chapter_to_tex(chapter: Chapter) -> str:
    chap_text = (
            r'\subparagraph*{%s}'
            '\n'
            % chapter.num
    )
    chap_text += ''.join(verse_to_tex(verse) for verse in chapter.verses)

    return chap_text


def testament_to_tex(testament: Iterator[Book]) -> str:
    testament_text = ""
    for book in testament:
        testament_text += tex_title(book.name)
        testament_text += ''.join(chapter_to_tex(chapter) for chapter in book.chapters)
        testament_text += "\\end{multicols}"
    return testament_text


def bible_to_tex(bible: Bible) -> str:
    text = "\\part{Old Testament}\n"
    text += testament_to_tex(bible.ot_books)
    text += "\n\\part{New Testament}\n"
    text += testament_to_tex(bible.nt_books)

    return text


def main():
    args = get_args()
    if args.bibletxt:
        src = Path(args.bibletxt).read_text(encoding='utf-8')
        bible = diff_to_bible(src)
    elif args.module:
        modules = SwordModules(args.module)
        sword = modules.get_bible_from_module(Path(args.module).stem)
        bible = sword_bible_to_bible(sword)
    else:
        raise ValueError('No Type Selected?')

    text = bible_to_tex(bible)

    template = MyTemplate((Path(__file__).parent.resolve() / 'template.tex').read_text(encoding='utf-8'))
    Path('generate.tex').write_text(template.substitute(books=text), encoding='utf-8')


if __name__ == '__main__':
    main()
