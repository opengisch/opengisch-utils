import yaml
import unicodedata

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
            if type(layer) is QgsVectorLayer:
                self.translate_layer_style_categories(layer)
                self.translate_layer_attribute_alias(layer)
                self.update_layer_style_categories_legend(layer, self.iface)

            # Translate layer name must be callled after style categories and
            # layer attributes
            self.translate_layer_name(layer)

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

        translation = self.dictionary.translate(
            'layer_name', 'all', layer.name())
        if translation:
            layer.setLayerName(translation)

    def translate_layer_style_categories(self, layer):
        # check if it's a vector layer
        if not type(layer) is QgsVectorLayer:
            return

        renderer = layer.rendererV2()
        if not type(renderer) is QgsCategorizedSymbolRendererV2:
            return

        categories = renderer.categories()

        for idx, cat in enumerate(categories):
            translation = self.dictionary.translate(
                'style_category', layer.name(), cat.label())
            if translation:
                renderer.updateCategoryLabel(idx, translation)

    def update_layer_style_categories_legend(self, layer, iface):
        legend = iface.legendInterface()
        legend.refreshLayerSymbology(layer)

    def translate_layer_group_name(self, layer, name):
        """Translate group name of a layer

        :param layer: The layer
        :param name: The group name
        :return: The translated name
        """
        # Remove the last part (project name in parentheses) of the group name
        proj_name = name[name.rfind(' ('):]
        only_group_name = name[:name.rfind(' (')]

        translation = self.dictionary.translate(
            'layer_group', 'all', only_group_name
        )

        return translation + proj_name

    def translate_layer_group_names(self, iface):
        """Translate all the groups names"""

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

    def translate(self, typez, context, word):
        """Translate a word.

        return the untranslated word if the translation is not in the dict"""

        # print('translation request: {} | {} | {}'.format(
        #    typez.encode('ascii', 'ignore'), context.encode('ascii', 'ignore'),
        #    word.encode('ascii', 'ignore')))

        # ===========
        # Uncomment to generate template yml
        #self._add_to_dictionary_template(typez, context, word)
        #return word
        # ===========

        try:
            trans = self.dictionary[typez][context][word]
            # print('returned translation: {}'.format(
            #    trans.encode('ascii', 'ignore')))
            return trans
        except Exception as e:
            # print('returned translation_e: {}'.format(
            #    word.encode('ascii', 'ignore')))
            return word

    # ================================================================

    def _add_to_dictionary_template(self, typez, context, word):
        """Create a dictionary template yaml with the requested words. The
        translation in the tempate will be the word with prefix FR_
        """
        template_dictionary = yaml.safe_load(open(
            '/home/mario/tmp/verivd/template_dict.yml'))

        if not template_dictionary:
            template_dictionary = {}

        try:
            template_dictionary[typez][context][word] = 'FR_'+word
        except:
            try:
                template_dictionary[typez][context] = {word: 'FR_'+word}
            except:
                template_dictionary[typez] = {context: {word: 'FR_'+word}}

        stream = file('/home/mario/tmp/verivd/template_dict.yml', 'w')

        stream.write(yaml.safe_dump(template_dictionary, default_flow_style =
        False, allow_unicode=True))

        stream.close()
