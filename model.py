from __future__ import annotations

from dataclasses import field, dataclass
import random
from typing import Type, cast

from faker import Faker
from faker_music import MusicProvider
from Data.Project.base import Dataset, Entity


# TODO replace this module with your own types

@dataclass
class RentalDataset(Dataset):
    people: list[Person]
    musics: list[Music]
    phonenumbers: list[Phone_number]
    transactions: list[Transaction]

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person, Music, Phone_number, Transaction]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return RentalDataset(
            cast(list[Person], entities[0]),
            cast(list[Music], entities[1]),
            cast(list[Phone_number], entities[2]),
            cast(list[Transaction], entities[3])
        )

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res = dict()
        res[Person] = self.people
        res[Music] = self.musics
        res[Phone_number] = self.phonenumbers
        res[Transaction] = self.transactions

        return res

    @staticmethod
    def generate(
            count_of_customers: int,
            count_of_musics: int,
            count_of_phonenumbers: int,
            count_of_transactions: int):

        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                            unique: bool = False, min_age: int = 0, max_age: int = 100) -> list[Person]:
            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(Person(
                    "P-" + (str(i).zfill(6)),
                    generator.name_male() if male else generator.name_female(),
                    random.randint(min_age, max_age),
                    male))

            return people

        def generate_musics(n: int, unique: bool = False) -> list[Music]:
            assert n > 0

            fake = Faker()
            fake.add_provider(MusicProvider)
            generator2 = fake if not unique else unique.fake
            musics = []
            for i in range(n):
                a = Music(generator2.music_genre(),
                          generator2.music_subgenre(),
                          generator2.music_instrument(),
                          generator2.music_instrument_category()
                          )
                musics.append(a)
            return musics

        def generate_phone_number(n: int) -> list[Phone_number]:
            assert n > 0

            fake = Faker()
            phn = []
            for i in range(n):
                c = Phone_number(fake.phone_number()
                                 )
                phn.append(c)
            return phn

        def generate_transactions(n: int, people: list[Person], musics: list[Music], phone_numbers: list[Phone_number]) -> list[
            Transaction]:
            assert n > 0
            assert len(people) > 0
            assert len(musics) > 0
            assert len(phone_numbers) > 0

            trips = []
            for i in range(n):
                person = random.choice(people)
                music = random.choice(musics)
                phone_number = random.choice(phone_numbers)
                trips.append(
                    Transaction(f"T-{str(i).zfill(6)}", phone_number.phone_number, person.id, music.genre, random.randint(100, 1000)))

            return trips

        people = generate_people(count_of_customers)
        musics = generate_musics(count_of_musics)
        phone_numbers = generate_phone_number(count_of_phonenumbers)
        transactions = generate_transactions(count_of_transactions, people, musics, phone_numbers)
        return RentalDataset(people, musics, phone_numbers, transactions)


@dataclass
class Transaction(Entity):
    id: str = field(hash=True)
    music: str = field(repr=True, compare=False)
    person: str = field(repr=True, compare=False)
    phone_number: str = field(repr=True, compare=False)
    length: int = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Transaction:
        return Transaction(seq[0], seq[1], seq[2], seq[3], int(seq[4]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.phone_number, self.person, self.music, str(self.length)]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "phone_number", "person", "music", "length"]

    @staticmethod
    def collection_name() -> str:
        return "transactions"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Transaction.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            phone_number CHAR(50) NOT NULL,
            person VARCHAR(8) NOT NULL,
            music VARCHAR(50) NOT NULL,
            length SMALLINT,

            FOREIGN KEY (phone_number) REFERENCES {Phone_number.collection_name()}(phone_number),
            FOREIGN KEY (person) REFERENCES {Person.collection_name()}(id),
            FOREIGN KEY (music) REFERENCES {Music.collection_name()}(genre)
        );
         """

@dataclass
class Phone_number(Entity):
    phone_number: str = field(hash=True)

    @staticmethod
    def from_sequence(seq: list[str]) -> Phone_number:
        return Phone_number(seq[0])

    def to_sequence(self) -> list[str]:
        return [self.phone_number]

    @staticmethod
    def field_names() -> list[str]:
        return ["phone_number"]

    @staticmethod
    def collection_name() -> str:
        return "phone_numbers"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Phone_number.collection_name()} (
            phone_number CHAR(50) NOT NULL PRIMARY KEY
        );
        """


@dataclass
class Music(Entity):
    genre: str = field(hash=True)
    subgenre: str = field(repr=True, compare=False)
    instrument: str = field(repr=True, compare=False)
    instrument_category: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Music:
        return Music(seq[0], seq[1], seq[2], seq[3])

    def to_sequence(self) -> list[str]:
        return [self.genre, self.subgenre, self.instrument, self.instrument_category]

    @staticmethod
    def field_names() -> list[str]:
        return ["genre", "subgenre", "instrument", "instrument_category"]

    @staticmethod
    def collection_name() -> str:
        return "musics"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Music.collection_name()} (
            genre VARCHAR(50) NOT NULL PRIMARY KEY,
            subgenre VARCHAR(50),
            instrument VARCHAR(50),
            instrument_category VARCHAR(50)
        );
        """


@dataclass
class Person(Entity):
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], int(seq[2]), bool(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, str(self.age), str(int(self.male))]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            name VARCHAR(50),
            age TINYINT,
            male BOOLEAN
        );
        """