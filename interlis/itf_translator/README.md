# ITFTranslator
ITFTranslator is a tool to translate interlis v1 transfer files (itf) in another language based on a text file 
dictionary. At the moment only German, French and Italian are supported, but in case it will be simple to add the 
support to other languages.

The main class is the `ITFTranslator` class in the module itf_translator_generic and permits to create a translator 
object based on a custom dictionary file. It is also possible to add custom tranlations rules.

Two extensions of `ITFTranslator` are already created with all the settings to translate DM01AVCH (federal cadastral 
surveying model) and MD01MOVD (Canton Vaud cadastral surveying model). The classes are `ITFTranslatorDM01AVCH` 
respectively  `ITFTranslatorMD01MOVD`  

## Dictionary files

The file is composed of line formatted like this:

`german_translation;french_tranlsation;italian_translation`

rules:
- blank lines are allowed
- line starting with '#' are ignored
- no spaces between words but underscores '_'

the line are readed from the top to the bottom. If a translation key is repeated, the last one will be used.


## Usage example

To translate the file `cad088_0616_V3mens.itf` based on the MD01MOVD model from French to German:

```
translator = ITFTranslatorMD01MOVD('/home/mario/cad088_0616_V3mens.itf')

translator.translate('cad088_0616_V3mens_DE.itf', ITFTranslator.LANGUAGE_FR, ITFTranslator.LANGUAGE_DE)
```

A file named `cad088_0616_V3mens_DE.itf` with the translation will be created. 