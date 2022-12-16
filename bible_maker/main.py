import argparse
import importlib
import json
from pathlib import Path
from string import Template
from typing import TypedDict, Callable, List, Dict, Optional

from bible_maker import paragraph
from bible_maker.tex import bible_to_tex


class MyTemplate(Template):
    """A template for `.tex` files

    https://stackabuse.com/formatting-strings-with-the-python-template-class/
    """

    delimiter = "$"


class Argument(TypedDict):
    """format.json"""
    long: str
    short: str
    help: str
    method: str


def get_args(arguments: List[Argument]):
    """Argument Parser wrapper"""
    parser = argparse.ArgumentParser(description="A software for generating bibles")
    parser.add_argument(
        "--paragrapher",
        "-p",
        required=False,
        help="select where the paragraphing json is",
    )

    options = parser.add_mutually_exclusive_group(required=True)
    for argument in arguments:
        options.add_argument(
            '--' + argument['long'],
            '-' + argument['short'],
            help=argument['help'],
            required=False,
        )

    return parser.parse_args()


def load_json(file: Path):
    return json.load(file.open("r", encoding="utf-8"))


def module_dir(filename: str) -> Path:
    """Opens a file in the same directory as the __main__"""
    return Path(__file__).parent.resolve() / filename


def get_method(path: str) -> Callable:
    """Returns a method from a module

    :param path: For example .bible_format_plugins.diff.args_to_bible
    :return: The function as a callable
    """
    parent = '.'.join(path.split('.')[:-1])
    method_name = path.split('.')[-1]
    module = importlib.import_module(parent, package='bible_maker')
    return getattr(module, method_name)


def get_function_path(args: Dict[str, str], available_arguments: List[Argument]) -> Optional[str]:
    """Works out which function needs to be used from the argument parser"""
    for arg_name, parsed_arg in args.items():
        if parsed_arg is not None and arg_name in {arg['long'] for arg in available_arguments}:
            arg = next((arg for arg in available_arguments if arg['long'] == arg_name))
            return arg['method']
    return None


def main():
    available_arguments: List[Argument] = load_json(module_dir('formats.json'))
    args = get_args(available_arguments)
    function_path = get_function_path(vars(args), available_arguments)
    if function_path is None:
        raise ValueError('Expected there to be a function available')

    method = get_method(function_path)

    bible = method(args)

    if args.paragrapher:
        paragraph.update_bible(bible, load_json(Path(args.paragrapher)))

    text = bible_to_tex(bible)

    template = MyTemplate(
        module_dir("template.tex").read_text(encoding="utf-8")
    )
    Path("generate.tex").write_text(template.substitute(books=text), encoding="utf-8")


if __name__ == "__main__":
    main()
