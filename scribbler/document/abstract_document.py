from abc import ABCMeta, abstractmethod
from enum import Enum


class AbstractDocument:
    __metaclass__ = ABCMeta

    def __init__(self, width, height, parent):
        self.parent = parent
        self.width = width
        self.height = height

    @abstractmethod
    def to_image(self):
        pass

    @abstractmethod
    def to_label(self):
        pass

    def get_size(self):
        if self.height is None:
            return self.parent.get_children_size()
        else:
            return self.width, self.height

    def get_children_size(self):
        return self.get_size()

    @abstractmethod
    def generate_random(self, index=-1):
        pass

    @abstractmethod
    def get_baselines(self):
        return []


class DocumentType(Enum):
    BACKGROUND = 0,
    TEXT = 1,
    IMAGE = 2
