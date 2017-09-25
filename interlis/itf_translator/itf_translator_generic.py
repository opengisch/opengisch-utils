"""This module contains ITFTranslator, Dictionary and SpecialCaseRule classe"""

# To call open with encoding in Python2 like in Python3
from io import open


class ITFTranslator(object):
    """Generic translator of itf (Interlis transfer format version 1) files"""

    LANGUAGE_DE = 0
    LANGUAGE_FR = 1
    LANGUAGE_IT = 2

    def __init__(self, itf_file_path, dictionary_file_path, rules=None):
        """Constructor.

        :param str itf_file_path:
            path of the itf file to translate

        :param str dictionary_file_path:
            path of the file containig the translations to be used

        :param list<SpecialCaseRule> rules:
            the optional list of translation rules to be applied
        """
        self.itf_file_path = itf_file_path
        self.dictionary_file_path = dictionary_file_path
        self.rules = rules

    def translate(self, output_file_path, language_from, language_to):
        """Translate the itf file

        :param str output_file_path:
            the path of the translated output file

        :param int language_from:
            the initial language. See the already defined class variables

        :param int language_to:
            the final language. See the already defined class variables
        """
        if not self.is_translatable(language_from, language_to):
            return False

        dictionary = Dictionary(
            self.dictionary_file_path, language_from, language_to)

        itf_file = open(self.itf_file_path, 'r', encoding='ISO-8859-1')
        output_file = open(output_file_path, 'w')
        data = itf_file.readlines()

        current_topic = None
        current_table = None

        for line in data:
            words = line.split()

            if words[0] in ['MODL', 'TOPI', 'TABL']:

                if words[0] == 'MODL':
                    current_topic = None
                elif words[0] == 'TOPI':
                    current_topic = words[1]
                    current_table = None
                if words[0] == 'TABL':
                    current_table = words[1]

                # search for rules
                from_rule = self.__get_translation_rule(
                    language_from, language_to, current_topic, current_table)

                if from_rule:
                    line = line.replace(words[1], from_rule)
                else:
                    line = line.replace(
                        words[1], dictionary.translate(words[1]))

            output_file.write(line)

        return True

    def __get_translation_rule(
            self, language_from, language_to, topic, table):
        """Return the translation rule relevant to the received
        arguments

        :param int language_from:
            the initial language. See the already defined class variables

        :param int language_to:
            the final language. See the already defined class variables

        :param str topic:
            the name of the topic

        :param str table:
            the name of the table

        :return str: the translation to be used or None if no rule is relevant
        """

        if not self.rules:
            return None

        for rule in self.rules:
            if (
                rule.language_from == language_from and
                rule.language_to == language_to and
                rule.topic == topic and
                rule.table == table
            ):
                return rule.translation

        return None

    def is_translatable(self, language_from, language_to):
        """Return if all the words of the itf_file are translatable and print
        eventually not found words

        :param int language_from:
            the initial language. See the already defined class variables

        :param int language_to:
            the final language. See the already defined class variables

        :return bool: True if translatable, False otherwise
        """

        result = True

        dictionary = Dictionary(
            self.dictionary_file_path, language_from, language_to)

        file_itf = open(self.itf_file_path, 'r', encoding='ISO-8859-1')
        data = file_itf.readlines()
        for line in data:
            words = line.split()

            if words[0] in ['MODL', 'TOPI', 'TABL']:
                try:
                    dictionary.translate(words[1])
                except KeyError:
                    result = False
                    print(
                        'Erorr, key not found: {} {}'.format(
                            words[0], words[1]))

        return result


class SpecialCaseRule:
    """Some translations are not always reversible. For example in the
    DM01AVCH model, french "element_lineaire" can be both german "linienelement"
    and "linienobjekt" depending of the topic. So it's possible to add some
    rules that defines how to translate words depending on the topic"""

    def __init__(self, language_from, language_to, topic, table, translation):
        """Constructor

        :param int language_from:
            the initial language. See the already defined class variables

        :param int language_to:
            the final language. See the already defined class variables

        :param str topic:
            the name of the topic

        :param str table:
            the name of the table

        :param str translation:
            the translation to use
        """

        self.language_from = language_from
        self.language_to = language_to
        self.topic = topic
        self.table = table
        self.translation = translation


class Dictionary:
    """This class represent the translation dictionary. It is created from a
    text file. The file is composed of line formatted like this:

        german_translation;french_tranlsation;italian_translation

    - blank lines are allowed
    - line starting with '#' are ignored
    - no spaces between words but underscores '_'

    the line are readed from the top to the bottom. If a translation key is
    repeated, the last one will be used.

    """

    def __init__(self, file_path, language_from, language_to):
        """Create the dictionary instance reading from the passed file and
        creating a dict with the desired languages

        :param str file_path:
            the path of the dictionary file

        :param int language_from:
            the initial language. See the already defined class variables

        :param int language_to:
            the final language. See the already defined class variables

        """

        self.dictionary = {}

        with open(file_path) as file:
            for line in file:
                # Allows blank lines and comments in dictionary files
                if line.strip() == '' or line.startswith('#'):
                    continue
                words = line.rstrip().split(';')
                self.dictionary[words[language_from]] = words[language_to]

    def translate(self, word):
        """Translate a word.

        :param str word:
            the word to be translated

        :return str:
            the translated word

        :raise KeyError: if the word is not present in the dict"""
        return self.dictionary[word]
