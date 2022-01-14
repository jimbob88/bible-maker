# Jimbob88's Bible Maker

This is a piece of software to help you generate your own copy of the bible!

## Guide

1. Download the copy of your bible from [Crosswire's Module Database](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles). I personally chose: [GerBoLut](http://crosswire.org/sword/modules/ModInfo.jsp?modName=GerBoLut)
2. Download a copy of schierlm's [BibleMultiConverter](https://github.com/schierlm/BibleMultiConverter). I'd recommend `BibleMultiConverter-AllInOneEdition-0.0.8.zip` (this is the current version available as of 14/01/2022)
3. Unzip your copy of BibleMultiConverter. This created the directory `C:\Users\black\Downloads\BibleMultiConverter-AllInOneEdition-0.0.8` on my system.
4. Unzip your Bible from crosswire into a folder of the same name `GerBoLut.zip -> .\GerBoLut`. Move this folder into the same folder as BibleMultiConverter
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
> python .\main.py -o .\<the name of your text file>.txt
```

11. Compile your `.tex` file in anyway you like!
    For example:

```
> pdflatex .\generate.tex
```

## Known Issues

- You can't mess and change the names of the books in the bible, because the `paragrapher` relies on these names to be the same, this could cause any number of issues if you start fiddling with stuff! This should be fixed sometime in the future!

## Screenshots

![Genesis in GerBoLut](https://i.imgur.com/fKZlg1p.png)

You may be wondering how this version of the bible has convenient breaks throughout the text (not in the PSALMS though), this is using the sister project [Carriage Return Bible Versifier](https://github.com/jimbob88/CR_bible) (also developed by me). After you have generated your first bible without these convenient line breaks, consider going over there and checking it out!

## Credits

- Thanks to [schierlm](https://github.com/schierlm) for his amazing [BibleMultiConverter](https://github.com/schierlm/BibleMultiConverter)
- Thanks to [The CrossWire Bible Society](https://crosswire.org/) for continuing to provide easy access to Bibles in many languages!
