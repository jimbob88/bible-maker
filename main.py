from collections import OrderedDict
import re
import itertools
import pprint as pp

from string import Template
class MyTemplate(Template):
    '''
    https://stackabuse.com/formatting-strings-with-the-python-template-class/
    '''
    delimiter = '$'

conversion_table = OrderedDict({
    "ot": OrderedDict([
        ("Gen", "Genesis"),
        ("Exod", "Exodus"),
        ("Lev", "Leviticus"),
        ("Num", "Numbers"),
        ("Deut", "Deuteronomy"),
        ("Josh", "Josh"),
        ("Judg", "Judges"),
        ("Ruth", "Ruth"),
        ("1Sam", "1 Samuel"),
        ("2Sam", "2 Samuel"),
        ("1Kgs", "1 Kings"),
        ("2Kgs", "2 Kings"),
        ("1Chr", "1 Chronicles"),
        ("2Chr", "2 Chronicles"),
        ("Ezra", "Ezra"),
        ("Neh", "Nehemiah"),
        ("Esth", "Esther"),
        ("Job", "Job"),
        ("Ps", "Psalms"),
        ("Prov", "Proverbs"),
        ("Eccl", "Ecclesiastes"),
        ("Song", "Song of Solomon"),
        ("Isa", "Isaiah"),
        ("Jer", "Jeremiah"),
        ("Lam", "Lamentations"),
        ("Ezek", "Ezekial"),
        ("Dan", "Daniel"),
        ("Hos", "Hosea"),
        ("Joel", "Joel"),
        ("Amos", "Amos"),
        ("Obad", "Obadiah"),
        ("Jonah", "Johnah"),
        ("Mic", "Micah"),
        ("Nah", "Nahum"),
        ("Hab", "Habakkuk"),
        ("Zeph", "Zephaniah"),
        ("Hag", "Haggai"),
        ("Zech", "Zechariah"),
        ("Mal", "Malachi"),
    ]),
    "nt": OrderedDict([
        ("Matt", "Matthew"),
        ("Mark", "Mark"),
        ("Luke", "Luke"),
        ("John", "John"),
        ("Acts", "Acts"),
        ("Rom", "Romans"),
        ("1Cor", "1 Corinthians"),
        ("2Cor", "2 Corinthians"),
        ("Gal", "Galatians"),
        ("Eph", "Ephesians"),
        ("Phil", "Philippians"),
        ("Col", "Colossians"),
        ("1Thess", "1 Thessalonians"),
        ("2Thess", "2 Thessalonians"),
        ("1Tim", "1 Timothy"),
        ("2Tim", "2 Timothy"),
        ("Titus", "Titus"),
        ("Phlm", "Philemon"),
        ("Heb", "Hebrews"),
        ("Jas", "James"),
        ("1Pet", "1 Peter"),
        ("2Pet", "2 Peter"),
        ("1John", "1 John"),
        ("2John", "2 John"),
        ("3John", "3 John"),
        ("Jude", "Jude"),
        ("Rev", "Revelation"),
    ]),
})
joined_conversion_table = OrderedDict()
joined_conversion_table.update(conversion_table['ot'])
joined_conversion_table.update(conversion_table['nt'])

# Generate in form: r"(Gen|Rev) (\d+):(\d)+ .*"
verse_regex = r"("+ '|'.join(joined_conversion_table)+ r") (\d+):(\d+) (.*)"
print(verse_regex)

with open('gerbolut.txt', 'r', encoding='utf-8') as f:
    bible = f.read()

versed = re.findall(verse_regex, bible, re.MULTILINE)
# versed_book = OrderedDict([(verse[0], verse[1:]) for verse in versed])
versed_book = OrderedDict([(item[0], list(item[1])) for item in itertools.groupby(versed, key=lambda x: x[0])])
# pp.pprint(versed_book)
# text = open('template.tex', 'r', encoding='utf-8').read()

text = ""

for book, verses in versed_book.items():
    book = joined_conversion_table[book]
    # print(book)
    text += (
        r'\part{%s}\pagebreak[1]'
        '\n'
        r'\begin{multicols}{2}'
        '\n' % book
    )
    for subsection in [(item[0], list(item[1])) for item in itertools.groupby(verses, key=lambda x: x[1]) ]:
        # print(subsection)
        text += (
            r'\subparagraph*{%s}'
            '\n'
            % subsection[0]
            )
        for verse in subsection[1]:
            text += (
                '$^{%s}$ %s\n'
                % (verse[2], verse[3])
            )
     
    text += (
        r'\end{multicols}'
        '\n'        
    )


with open('generate.tex', 'w', encoding='utf-8') as f:
    temp = MyTemplate(open('template.tex', 'r', encoding='utf-8').read())
    f.write(temp.substitute(books=text))

print(text[:1000000])

# text = r"""
# \begin{multicols}{2}
# [
# \section{First Section}
# All human things are subject to decay. And when fate summons, Monarchs must obey.
# ]
# \blindtext\blindtext
# \end{multicols}
# """
# print(text)