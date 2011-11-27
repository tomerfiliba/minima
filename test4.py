class FormField(object):
    def __init__(self, label, type, validator = lambda x: x):
        self.label = label
        self.type = type
        self.validator = validator

class Form(object):
    def __init__(self, *fields):
        self.fields = list(fields)
    def render(self, doc):
        with doc.block("table"):
            for f in self.fields:
                with doc.block("tr"):
                    with doc.block("td"):
                        doc.text(f.label)
                    with doc.block("td"):
                        doc.elem("input", type="text")



