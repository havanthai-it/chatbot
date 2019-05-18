import yaml


class DomainYmlReader:
    """Read domain.yml file"""

    def __init__(self):
        self.entities = []
        self.slots = []
        self.intents = []
        self.actions = []
        self.templates = {}
        self.current_section_name = ""

    def read(self, stream):
        self.__init__()
        result = yaml.safe_load(stream)
        return result

