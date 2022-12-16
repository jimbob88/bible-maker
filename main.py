import argparse
import json
from pathlib import Path
from string import Template

from pysword.modules import SwordModules

from bible_maker.bible_format_plugins.diff import diff_to_bible
from bible_maker.bible_format_plugins.sword import sword_bible_to_bible
from bible_maker.tex import bible_to_tex


class MyTemplate(Template):
    """A template for `.tex` files

    https://stackabuse.com/formatting-strings-with-the-python-template-class/
    """

    delimiter = "$"


def get_args():
    """Argument Parser wrapper"""
    parser = argparse.ArgumentParser(description="A software for generating bibles")
    parser.add_argument(
        "--paragrapher",
        "-p",
        required=False,
        help="select where the paragraphing json is",
    )

    options = parser.add_mutually_exclusive_group()

    options.add_argument(
        "--module",
        "-m",
        required=False,
        help="Choose which bible SWORD module zip to use",
    )
    options.add_argument(
        "--bibletxt",
        "-b",
        required=False,
        help="Choose which bible DIFFABLE you will use",
    )

    return parser.parse_args()


def load_json(file: str):
    return json.load(Path(file).open("r", encoding="utf-8"))


def main():
    args = get_args()
    if args.bibletxt:
        src = Path(args.bibletxt).read_text(encoding="utf-8")
        bible = diff_to_bible(src)
    elif args.module:
        modules = SwordModules(args.module)
        sword = modules.get_bible_from_module(Path(args.module).stem)
        bible = sword_bible_to_bible(sword)
    else:
        raise ValueError("No Type Selected?")

    text = bible_to_tex(bible)

    template = MyTemplate(
        (Path(__file__).parent.resolve() / "template.tex").read_text(encoding="utf-8")
    )
    Path("generate.tex").write_text(template.substitute(books=text), encoding="utf-8")


if __name__ == "__main__":
    main()
