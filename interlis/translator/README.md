Usage example:

```
    translator = ITFTranslatorMD01MOVD(
        '/home/mario/cad088_0616_V3mens.itf'
    )

    translator.translate(
        'cad088_0616_V3mens_DE.itf', ITFTranslator.LANGUAGE_FR, ITFTranslator.LANGUAGE_DE)
```