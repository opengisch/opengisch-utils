import yaml

from qgis.core import (
    QgsProject, QgsCategorizedSymbolRendererV2, QgsLayerTreeGroup,
    QgsVectorLayer)


class QgisLayersTranslator(object):
    """Translate the loaded QGIS layer on the fly. Translate layer names,
    attribute aliases, group names, style categories"""

    def __init__(self, iface, dictionary):
        self.iface = iface
        self.dictionary = dictionary

    def run(self):
        layers = self.iface.legendInterface().layers()

        for layer in layers:
            print('layer: {}, type: {}'.format(layer.name(), type(layer)))
            if type(layer) is QgsVectorLayer:
                self.translate_layer_style_categories(layer)
                self.translate_layer_attribute_alias(layer)
                self.update_layer_style_categories_legend(layer, self.iface)

            # Translate layer name must be callled after style categories and
            # layer attributes
            self.translate_layer_name(layer)


                # TODO make this at the end of the layer loading, but how?
        # translate_layer_group_name(iface)

    def translate_layer_attribute_alias(self, layer):
        """Translate the attributes of the layer adding aliases"""

        # attribute alias

        for attribute_idx in layer.attributeList():
            translation = self.dictionary.translate(
                'layer_attribute', layer.name(), layer.attributeDisplayName(
                attribute_idx))
            if translation:
                layer.addAttributeAlias(attribute_idx, translation)

        return

    def translate_layer_name(self, layer):
        """Translate the layer name"""

        print('translate_layer_name: {}'.format(layer.name()))
        translation = self.dictionary.translate(
            'layer_name', 'all', layer.name())
        if translation:
            layer.setLayerName(translation)

    def translate_layer_style_categories(self, layer):

        print('cat layer: {}'.format(layer.name()))
        # check if it's a vector layer
        if not type(layer) is QgsVectorLayer:
            return

        print('cat layer rend: {}'.format(layer.rendererV2()))

        renderer = layer.rendererV2()
        if not type(renderer) is QgsCategorizedSymbolRendererV2:
            return

        print('cat layer: {}'.format(layer.name()))

        categories = renderer.categories()

        for idx, cat in enumerate(categories):
            translation = self.dictionary.translate(
                'style_category', layer.name(), cat.label())
            if translation:
                renderer.updateCategoryLabel(idx, translation)

    def update_layer_style_categories_legend(self, layer, iface):
        legend = iface.legendInterface()
        legend.refreshLayerSymbology(layer)

    # TODO add method to translate single group name

    def translate_layer_group_name(self, iface):
        root = QgsProject.instance().layerTreeRoot()
        for child in root.children():
            if isinstance(child, QgsLayerTreeGroup):
                translation = self.dictionary.translate(
                    'layer_group', 'all', child.name())
                if translation:
                    child.setName(translation)


class Dictionary:
    """This class represent the translation dictionary. It is created from a
    yaml file.
    """

    def __init__(self, file_path):
        """Create the dictionary instance reading from the passed file"""

        try:
            self.dictionary = yaml.safe_load(open(file_path))

        except Exception as e:
            print(e)

    def translate(self, type, context, word):
        """Translate a word.

        return the untranslated word if the translation is not in the dict"""

        # TODO remove. Only for test
        #print(type, context, word)
        #self._add_to_dictionary_template(type, context, word)
        #return word
        # ----

        try:
            trans = self.dictionary[type][context][word]
            return trans
        except:
            return word                                                                 
    # ================================================================

    def _add_to_dictionary_template(self, type, context, word):
        """Create a dictionary template yaml with the requested words. The
        translation in the tempate will be the word with prefix X
        """

        template_dictionary = yaml.safe_load(open(
            '/home/mario/tmp/verivd/template_dict.yml'))

        if not template_dictionary:
            template_dictionary = {}

        try:
            template_dictionary[type][context][word] = 'FR_'+word
        except:
            try:
                template_dictionary[type][context] = {word: 'FR_'+word}
            except:
                template_dictionary[type] = {context: {word: 'FR_'+word}}

        #print(template_dictionary)

        stream = file('/home/mario/tmp/verivd/template_dict.yml', 'w')

        stream.write(yaml.safe_dump(template_dictionary, default_flow_style =
        False))

        stream.close()

    def XXget_translation(self, type, context, text):
    # TODO remove. Created only for test

        if text == 'art':
            return 'genre'
        elif text == 'qualitaet_txt':
            return 'qualite_txt'
        elif text == 'EO Linienelemente':
            return 'Proba layer name'
        elif text == 'restliche EO-Arten':
            return 'trrr rest EO-qualcosa'
        elif text == 'befestigt.Bahn':
            return 'befe trein'
        elif text == 'AV Allgemein (verivd_20170913_0950)':
            return 'Uella'
        else:
            return None


if __name__ == '__main__':
    dictionary_verivd = Dictionary('/home/mario/Dropbox/workspace/veriso/modules/verivd/translations_verivd.yml')

    dictionary_verivd._add_to_dictionary_template('one', 'two', 'three')
    dictionary_verivd._add_to_dictionary_template('one', 'two', 'four')
    dictionary_verivd._add_to_dictionary_template('one', 'two', 'five')
    dictionary_verivd._add_to_dictionary_template('one', 'six', 'seven')
    dictionary_verivd._add_to_dictionary_template('one', 'eight', 'nine')
    #print(dictionary_verivd.translate('Layer', 'Base', 'EO Punktelemente'))
