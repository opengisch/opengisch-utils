import os
from itf_translator_generic import ITFTranslator
from itf_translator_generic import SpecialCaseRule


class ITFTranslatorDM01AVCH(ITFTranslator):
    """Extend ITFTranslator with arguments already set to translate DM01AVCH,
    the national model"""

    def __init__(self, itf_file_path):
        """Constructor.

        :param str itf_file_path:
            path of the itf file to translate
        """

        rules = [
            # FR->DE
            SpecialCaseRule(
                ITFTranslator.LANGUAGE_FR, ITFTranslator.LANGUAGE_DE,
                'Bords_de_plan', 'Element_lineaire', 'Linienobjekt'),
            # IT->DE
            SpecialCaseRule(
                ITFTranslator.LANGUAGE_IT, ITFTranslator.LANGUAGE_DE,
                'Margine_del_piano', 'Elemento_lineare', 'Linienobjekt'),
            # DE->FR
            SpecialCaseRule(
                ITFTranslator.LANGUAGE_DE, ITFTranslator.LANGUAGE_FR,
                'Bodenbedeckung', 'Objektname', 'Nom_objet'),
            SpecialCaseRule(
                ITFTranslator.LANGUAGE_DE, ITFTranslator.LANGUAGE_FR,
                'Bodenbedeckung', 'ObjektnamePos', 'PosNom_objet'),
            # IT-FR
            SpecialCaseRule(
                ITFTranslator.LANGUAGE_DE, ITFTranslator.LANGUAGE_FR,
                'Copertura_del_suolo', 'Nome_Oggetto', 'Nom_objet'),
            SpecialCaseRule(
                ITFTranslator.LANGUAGE_DE, ITFTranslator.LANGUAGE_FR,
                'Copertura_del_suolo', 'PosNome_Oggetto', 'PosNom_objet')
        ]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        dictionary_file = os.path.join(
            current_dir, 'dictionary_data', 'translations_DM01AVCH.txt')

        super(ITFTranslatorDM01AVCH, self).__init__(
            itf_file_path, dictionary_file,
            rules
        )
