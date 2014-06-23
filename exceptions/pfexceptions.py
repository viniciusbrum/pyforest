"""
Created on 21/06/2014

@author: vinicius
"""


class PFTypeError(TypeError):
    """classdocs"""

    def __init__(self, attribute, expected_types):
        """Constructor"""
        self.value = attribute + ' must be instance of ' + expected_types

    def __str__(self):
        return repr(self.value)
