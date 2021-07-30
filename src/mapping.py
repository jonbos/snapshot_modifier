import itertools
from abc import ABC


class Mapping(ABC):
    attributes = None
    tag_name = None

    def __init__(self, row):
        self.old_name = row["old_name"]
        self.new_name = row["new_name"]

    def apply(self, soup):
        if elements := soup.find_all(self.tag_name, {attr: self.old_name for attr in self.attributes}):
            for element, attribute in itertools.product(elements, self.attributes):
                element[attribute] = self.new_name
        return soup


class UserMapping(Mapping):
    attributes = ["name", "nativeId"]
    tag_name = "users"


class GroupMapping(Mapping):
    attributes = ["name", "nativeId"]
    tag_name = "groups"


class ResolutionMapping(Mapping):
    attributes = ["name"]
    tag_name = "resolutions"
