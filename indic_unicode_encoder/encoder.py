import json
import math
import sys
import pandas as pd
from typing import Optional


def sanitize_str(data: str):
    return data.strip().replace("\u200c", "")


def read_csv_to_list(filename: str) -> list[dict[str, str | float | None]]:
    ext = filename.split(".")[-1]
    match ext:
        case "json":
            with open(filename, "r") as f:
                raw_json = f.read()
                return json.loads(raw_json)

        case "csv":
            df = pd.read_csv(filename)
            return df.to_dict("records")

        case _:
            raise AttributeError(
                f"Unable to load unsupported  filetype detected: {ext}. Please use files of type csv or json "
            )


class EncodingMapping:
    alphabet: str
    consonant: Optional[str]
    signs: Optional[str]

    def __init__(self, alphabet: str, consonant: str | None, signs: str | None) -> None:
        self.alphabet = alphabet
        self.consonant = consonant
        self.signs = signs

    @staticmethod
    def from_dict(data: dict):
        alphabet = data["alphabet"]
        consonant = data["consonant"]
        signs = data["signs"]

        if alphabet is None or (type(alphabet) == float and math.isnan(alphabet)):
            raise AttributeError(f"Missing value for alphabet in dict: {data}")
        else:
            alphabet = sanitize_str(str(alphabet))

        if type(consonant) == float and math.isnan(consonant):
            consonant = None
        else:
            consonant = sanitize_str(str(consonant))

        if type(signs) == float and math.isnan(signs):
            signs = None
        else:
            signs = sanitize_str(str(signs))

        return EncodingMapping(alphabet, consonant, signs)


class Encoder:
    mappings: list[EncodingMapping]
    sign_priorities: list[str]
    prefix_signs: set[str]
    __mappings_avilable_for: set[str]

    def __init__(
        self,
        mappings: list[EncodingMapping],
        sign_priorities: list[str],
        prefix_signs: list[str],
    ) -> None:
        self.mappings = mappings
        self.sign_priorities = sign_priorities
        self.prefix_signs = set(prefix_signs)

        self.__mappings_avilable_for = set([mapping.alphabet for mapping in mappings])

    def __get_priority(self, sign: str):
        try:
            return self.sign_priorities.index(sign)
        except ValueError:
            # return max unicode value supported by python if sign not found
            return sys.maxunicode

    def __sort_signs(self, signs: list[str]):
        return sorted(signs, key=lambda s: self.__get_priority(s))

    def __sign_string(self, signs: list[str]):
        sorted_signs = self.__sort_signs(signs)
        return "".join(sorted_signs)

    def to_unicode(self, data: str):
        encoded_sentence = ""
        signs = []
        prefix_signs = []

        for char in data:
            if char not in self.__mappings_avilable_for:
                encoded_sentence += self.__sign_string(signs) + char
                signs = []
                prefix_signs = []
                continue

            matching_mapping = next(
                (mapping for mapping in self.mappings if mapping.alphabet == char)
            )

            is_composite_map = (
                matching_mapping.consonant is not None
                and matching_mapping.signs is not None
            )

            if matching_mapping.signs is not None:
                for sign in matching_mapping.signs:
                    # Composite maps always apply signs after consonant
                    if is_composite_map:
                        prefix_signs.append(sign)
                    elif sign in self.prefix_signs:
                        prefix_signs.append(sign)
                    else:
                        signs.append(sign)

            if matching_mapping.consonant is not None:
                encoded_sentence += (
                    self.__sign_string(signs) + matching_mapping.consonant
                )
                signs = prefix_signs
                prefix_signs = []
        return encoded_sentence + self.__sign_string(signs)


class EncoderBuilder:
    __mappings_file: Optional[str]
    __priorities_file: Optional[str]
    __prefix_file: Optional[str]

    def __init__(self) -> None:
        self.__mappings_file = None
        self.__priorities_file = None
        self.__prefix_file = None

    def mappings_file(self, mappings_file):
        self.__mappings_file = mappings_file
        return self

    def priorities_file(self, priorities_file):
        self.__priorities_file = priorities_file
        return self

    def prefix_file(self, prefix_file):
        self.__prefix_file = prefix_file
        return self

    def build(self) -> Encoder:
        if (
            self.__mappings_file is None
            or self.__prefix_file is None
            or self.__priorities_file is None
        ):
            raise TypeError(
                "Builder requires all of mappings_file, prefix_file and priorities_file to be specified"
            )

        # Read the files and sanitize the data
        mappings = list(
            map(
                EncodingMapping.from_dict,
                read_csv_to_list(self.__mappings_file),
            )
        )

        priorities = list(
            map(
                lambda data: sanitize_str(str(data["unicode"]))[0],
                read_csv_to_list(self.__priorities_file),
            )
        )

        prefix_signs = list(
            map(
                lambda data: sanitize_str(str(data["unicode"]))[0],
                read_csv_to_list(self.__prefix_file),
            )
        )

        return Encoder(mappings, priorities, prefix_signs)

    def __call__(self):
        return self.build()
