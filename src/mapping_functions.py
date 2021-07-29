import re
from abc import ABC


class MappingFunction(ABC):
    find_str = None
    replace_str = None

    def apply(self, text: str) -> str:
        return re.sub(self.find, self.replace, text)

    def __init__(self, row):
        self.find = r'%s' % (self.find_str.format_map(row))
        self.replace = r'%s' % (self.replace_str.format_map(row))


class GroupMappingFunction(MappingFunction):
    find_str = '<groups nativeId="{old_name}" name="{old_name}"/>'
    replace_str = '<groups nativeId="{new_name}" name="{new_name}"/>'


class UserMappingFunction(MappingFunction):
    find_str = '<groups nativeId="{old_name}" name="{old_name}"/>'
    replace_str = '<groups nativeId="{new_name}" name="{new_name}"/>'


class ResolutionMappingFunction(MappingFunction):
    find_str = '<groups nativeId="{old_name}" name="{old_name}"/>'
    replace_str = '<groups nativeId="{new_name}" name="{new_name}"/>'
