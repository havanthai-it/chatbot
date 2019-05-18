class Message(object):
    def __init__(self, text, data=None, time=None, output_properties=None):
        self.text = text
        self.data = data if data else {}
        self.time = time
        if output_properties:
            self.output_properties = output_properties
        else:
            self.output_properties = set()

    def set(self, prop, info, add_to_output=False):
        self.data[prop] = info
        if add_to_output:
            self.output_properties.add(prop)

    def get(self, prop):
        if prop in self.data:
            return self.data[prop]
        else:
            return None
