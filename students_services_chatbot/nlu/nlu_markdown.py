import re
import logging

from nlu.objects.message import Message
from nlu.objects.training_data import TrainingData

logger = logging.getLogger(__name__)

INTENT = "intent"
SYNONYM = "synonym"
REGEX = "regex"
LOOKUP = "lookup"
available_sections = [INTENT, SYNONYM, REGEX, LOOKUP]

ent_regex = re.compile(r'\[(?P<entity_text>[^\]]+)'
                       r'\]\((?P<entity>[^:)]*?)'
                       r'(?:\:(?P<value>[^)]+))?\)')  # [entity_text](entity_type(:entity_synonym)?)
item_regex = re.compile(r'\s*[-\*+]\s*(.+)')


class NluMarkdownReader:
    """Read markdown training data"""

    def __init__(self):
        self.current_section = None
        self.current_title = None
        self.lookup_tables = []
        self.training_examples = []
        self.entity_synonyms = {}
        self.regex_features = []
        self.section_regexes = self._create_section_regexes(available_sections)
        self.lookup_tables = []

    def read(self, s):
        """Read markdown string"""
        self.__init__()
        for line in s.splitlines():
            line = line.strip()
            header = self._find_section_header(line)
            if header is not None:
                self._set_current_section(header[0], header[1])
            else:
                self._parse_item(line)

        # ### Inspect: todo
        # print(">> entity_synonyms:")
        # print(self.entity_synonyms)
        # print("-------------------")
        # print(">> training_examples:")
        # for example in self.training_examples:
        #     print(example.text)
        #     print(example.data)
        #     print("---")
        # print("-------------------")
        return TrainingData(self.training_examples, self.entity_synonyms,
                            self.regex_features, self.lookup_tables)

    @staticmethod
    def _create_section_regexes(section_names):
        def make_regex(sn):
            return re.compile(r'##\s{}:(.+)'.format(sn))

        return {sn: make_regex(sn) for sn in section_names}

    def _find_section_header(self, line):
        """Check if current line contains a section header and return header section"""
        for name, regex in self.section_regexes.items():
            match = re.match(regex, line)
            if match is not None:
                return name, match.group(1)

        return None

    def _set_current_section(self, section, title):
        """Update parsing mode."""
        if section not in available_sections:
            raise ValueError("Found markdown section {} which is not "
                             "in the allowed sections {},".format(section, ",".join(available_sections)))

        self.current_section = section
        self.current_title = title.strip()

    def _parse_item(self, line):
        """Parses an md list item line based on the current section type."""
        match = re.match(item_regex, line)
        if match:
            item = match.group(1)
            if self.current_section == INTENT:
                parsed = self._parse_training_example(item)
                self.training_examples.append(parsed)
            elif self.current_section == SYNONYM:
                self._add_synonym(item, self.current_title)
            elif self.current_section == REGEX:
                self.regex_features.append(
                    {"name": self.current_title, "pattern": item})
            elif self.current_section == LOOKUP:
                self._add_item_to_lookup(item)

    def _parse_training_example(self, example):
        """Extract entities and synonyms, and convert to plain text."""
        entities = self._find_entities_in_training_example(example)
        plain_text = re.sub(ent_regex, lambda m: m.groupdict()['entity_text'], example)
        self._add_synonyms(plain_text, entities)
        message = Message(plain_text, {'intent': self.current_title})
        if len(entities) > 0:
            message.set('entities', entities)
        return message

    @staticmethod
    def _find_entities_in_training_example(example):
        """Extracts entities from a markdown intent example."""
        entities = []
        offset = 0
        for match in re.finditer(ent_regex, example):
            entity_text = match.groupdict()['entity_text']
            entity_type = match.groupdict()['entity']
            entity_value = match.groupdict()['value'] if match.groupdict()['value'] else entity_text

            start_index = match.start() - offset
            end_index = start_index + len(entity_text)
            offset += len(match.group(0)) - len(entity_text)

            entity = {
                "start": start_index,
                "end": end_index,
                "value": entity_value,
                "entity": entity_type
            }
            entities.append(entity)

        return entities

    def _add_synonyms(self, plain_text, entities):
        """Adds synonyms found in intent examples"""
        for e in entities:
            e_text = plain_text[e['start']:e['end']]
            if e_text != e['value']:
                self._add_synonym(e_text, e['value'])

    def _add_synonym(self, text, value):
        if text in self.entity_synonyms and self.entity_synonyms[text] != value:
            logger.warning("Found inconsistent entity synonyms while {0}, overwriting {1}->{2}"
                           "with {1}->{2} during merge".format("reading markdown", text,
                                                               self.entity_synonyms[text], value))
        self.entity_synonyms[text] = value

    def _add_item_to_lookup(self, item):
        """Takes a list of lookup table dictionaries.  Finds the one associated
        with the current lookup, then adds the item to the list."""
        matches = [l for l in self.lookup_tables
                   if l["name"] == self.current_title]
        if not matches:
            self.lookup_tables.append({"name": self.current_title, "elements": [item]})
        else:
            elements = matches[0]['elements']
            elements.append(item)
