from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type


class Entity(ABC):
    """
    A class that represents a type which can be managed with our library.
    """

    @staticmethod
    @abstractmethod
    def from_sequence(seq: list[str]) -> Entity:
        """
        Returns an instance from a sequence of string values.
        :param seq: the sequence of values
        :return: the instance
        """
        pass

    @abstractmethod
    def to_sequence(self) -> list[str]:
        """
        Returns a sequence of string values that describe the state of the type.
        :return: the sequence of values
        """
        pass

    @staticmethod
    @abstractmethod
    def field_names() -> list[str]:
        """
        Returns the list of field (attribute) names.
        :return: the list of names
        """
        pass

    @staticmethod
    @abstractmethod
    def collection_name() -> str:
        """
        Returns the name of the collection which can be used as the name of a file, a sheet or a table.
        :return: the name
        """
        pass

    @staticmethod
    @abstractmethod
    def create_table() -> str:
        """
        Returns a CREATE TABLE SQL statement which creates the table.
        :return: the statement
        """
        pass


class Dataset(ABC):
    """
    Represents a data set which consists of multiple types.
    """

    @abstractmethod
    def entities(self) -> dict[Type[Entity], list[Entity]]:
        """
        Returns the dictionary of entities. The keys are the types, and the values are the corresponding lists of objects.
        :return: the dictionary
        """
        pass

    @staticmethod
    @abstractmethod
    def entity_types() -> list[Type[Entity]]:
        """
        Returns the list of entity types.
        :return: the list of types
        """
        pass

    @staticmethod
    @abstractmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        """
        Returns an instance from a sequence of entity lists.
        :param entities: the entities
        :return: the instance
        """
        pass

    @staticmethod
    @abstractmethod
    def generate(**kwargs):
        """
        Generates a dataset with the use of the given parameters. Parameters are being defined by the implementations.
        :param kwargs: the parameter values
        :return: the instance
        """
        pass