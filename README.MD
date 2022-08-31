# Jimbob88's Bible Maker

This is a piece of software to help you generate your own copy of the bible!

## Initial setup

```commandline
pip install -r requirements.txt
```


## Using a zip - Guide
1. Download the copy of your bible from [Crosswire's Module Database](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles). I personally chose: [GerBoLut](http://crosswire.org/sword/modules/ModInfo.jsp?modName=GerBoLut)
2. Save the location of `[bible_id].zip`
3. Execute `main.py`
```commandline
python main.py --module [bible_id].zip
```
4. Compile the `generate.tex` file. For example:
```commandline
latexmk -pvc -pdf -xelatex -interaction=nonstopmode generate.tex 
```

## Using a Diff - Guide (Alternative Method)

1. Download the copy of your bible from [Crosswire's Module Database](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles). I personally chose: [GerBoLut](http://crosswire.org/sword/modules/ModInfo.jsp?modName=GerBoLut)
2. Download a copy of schierlm's [BibleMultiConverter](https://github.com/schierlm/BibleMultiConverter). I'd recommend `BibleMultiConverter-AllInOneEdition-0.0.8.zip` (this is the current version available as of 29/08/2022)
3. Unzip your copy of BibleMultiConverter. This created the directory `C:\Users\black\Downloads\BibleMultiConverter-AllInOneEdition-0.0.8` on my system.
4. <s>Unzip your Bible from crosswire into a folder of the same name `GerBoLut.zip -> .\GerBoLut`. 
Move this folder into the same folder as BibleMultiConverter (WARNING: This is not the correct method as of 16/01/2022, you need to install this bible as a module, to do this easily download a copy of [Bible Time](https://bibletime.info/) and install your bible from there)</s>
Extract from the downloaded zip (i.e. `gerbolut.zip`): `/modules/texts/ztext/`. For `GerBoLut` this meant I now had a file called `GerBoLut` containing both `ot` and `nt` files (i.e. `nt.bzz`)
5. Open a commandline window in the directory which contains `BibleMultiConverter-AllInOneEdition.jar`. (Shift+Right-Click `Open PowerShell window here`)
6. Generate a "Diffable" file:
   For example, if I was doing this for `GerBoLut`:

```
> java -jar .\BibleMultiConverter-AllInOneEdition.jar SWORD .\GerBoLut\ Diffable .\gerbolut.txt
```

The general form would be:

```
> java -jar .\BibleMultiConverter-AllInOneEdition.jar SWORD .\<FOLDER CONTAINING modules DIRECTORY>\ Diffable .\<any text file name>.txt
```

7. Download a copy of my bible maker!
8. Copy your text file to the same directory and open a new powershell window here (as seen in 5.)
9. Open the `template.tex` file and change the author, date, name as you like!
10. Generate your bible tex file:

```
> python .\main.py -b .\<the name of your text file>.txt
```

11. Compile your `.tex` file in any way you like!
    For example:

```
> pdflatex .\generate.tex
```

## Known Issues

- You can't mess and change the names of the books in the bible, because the `paragrapher` relies on these names to be the same, this could cause any number of issues if you start fiddling with stuff! This should be fixed sometime in the future!
- If you don't have much memory `pdflatex` can sometimes fail

## Screenshots

![Genesis in GerBoLut](https://i.imgur.com/fKZlg1p.png)

You may be wondering how this version of the bible has convenient breaks throughout the text (not in the PSALMS though), this is using the sister project [Carriage Return Bible Versifier](https://github.com/jimbob88/CR_bible) (also developed by me). After you have generated your first bible without these convenient line breaks, consider going over there and checking it out!

## Credits

- Thanks to [schierlm](https://github.com/schierlm) for his amazing [BibleMultiConverter](https://github.com/schierlm/BibleMultiConverter)
- Thanks to [The CrossWire Bible Society](https://crosswire.org/) for continuing to provide easy access to Bibles in many languages!


## Usage
```commandline
usage: main.py [-h] [--module MODULE] [--bibletxt BIBLETXT] [--paragrapher PARAGRAPHER]

A software for generating bibles

optional arguments:
  -h, --help            show this help message and exit
  --module MODULE, -m MODULE
                        Choose which bible SWORD module zip to use
  --bibletxt BIBLETXT, -b BIBLETXT
                        Choose which bible DIFFABLE you will use
  --paragrapher PARAGRAPHER, -p PARAGRAPHER
                        select where the paragraphing json is
```