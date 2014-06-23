class PFTypeError(TypeError):

    def __init__(self, attribute, expected_types):
        self.value = attribute + ' must be instance of ' + expected_types

    def __str__(self):
        return repr(self.value)
