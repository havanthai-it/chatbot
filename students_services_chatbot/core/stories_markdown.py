class StoriesMarkdownReader:
    """Read stories data from markdown file"""
    """
    IDEA:
    - each line is a training example
    - when start read a block(a story), init [None, None, None, None, None]
    - then handle each line:
        training example 1: [None, None, None, None, {..action_listen..}, {intent: user_intent_great,...}]
        training example 2: [None, None, None, {..action_listen}, {..., user_intent_great: hello,...}, {..., utter_greet: Hi,...}]
        ...
    """

    def __init__(self):
        self.current_block_name = ""
        self.content = {}

    def read(self, s):
        """Read markdown string"""

        self.__init__()
        for line in s.splitlines():
            line = line.strip()
            if len(line) > 2:
                self._parse_line(line)

        return self.content

    def _parse_line(self, line):
        if line[0:2] == "##":
            self.current_block_name = line[2:].strip()
            self.content[self.current_block_name] = []
        elif line[0:2] == "* ":
            self.content[self.current_block_name].append({
                "type": "intent",
                "value": line[2:]
            })
        elif line[0:2] == "- ":
            self.content[self.current_block_name].append({
                "type": "action",
                "value": line[2:]
            })
