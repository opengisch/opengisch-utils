# ITFTranslator
*ITFTranslator* is a tool to translate Interlis v1 transfer files (itf) into another language based on a text file 
dictionary. 

A program developed by Swisstopo called _DM01AVCH_Translator_ already exists to translate federal model's itf files. 
The program was developed in 2008 by Swisstopo. Unfortunately, it only works on Windows 
and it can't be completely automated because of the necessary interaction with the GUI and the need to make some manual 
adjustments to the output file.
                               
_ITFTranslator_ has been developed to overcome these limitations. 

## Structure

The main class is the `ITFTranslator` class in the module itf_translator_generic and permits to create a translator 
object based on a custom dictionary file. It is also possible to add custom translations rules.

Two extensions of `ITFTranslator` are already created with all the settings to translate DM01AVCH (federal cadastral 
surveying model) and MD01MOVD (Canton Vaud cadastral surveying model). The classes are `ITFTranslatorDM01AVCH` 
respectively  `ITFTranslatorMD01MOVD`  

## Dictionary files

The file is composed of line formatted like this:

`german_translation;french_tranlsation;italian_translation`

rules:
- blank lines are allowed
- line starting with '#' are ignored

the lines are readed from the top to the bottom. If a translation key is repeated, the last one will be used.

At the moment only German, French and Italian are supported, but in case it will be simple to add the 
support to other languages.

The existing dictionaries for ITFTranslatorDM01AVCH and ITFTranslatorMD01MOVD are based on the dictionary used by the 
Swisstopo's tool DM01AVCH_Translator tool.

## Usage example

To translate the file `cad088_0616_V3mens.itf` based on the MD01MOVD model from French to German:

```
translator = ITFTranslatorMD01MOVD('/home/mario/cad088_0616_V3mens.itf')

translator.translate('cad088_0616_V3mens_DE.itf', ITFTranslator.LANGUAGE_FR, ITFTranslator.LANGUAGE_DE)
```

A file named `cad088_0616_V3mens_DE.itf` with the translation will be created. 