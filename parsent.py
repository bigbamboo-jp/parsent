import copy
import re
from enum import IntEnum, auto
from typing import Self


class DelimiterHandlingMode(IntEnum):
    REMOVE = auto()
    ADDITIONAL_TO_AROUND = auto()
    ADDITIONAL_TO_BODY = auto()


class SentenceStructureInformation():
    def __init__(self, sentence, structure_data) -> None:
        self._sentence = sentence
        self._structure_data = copy.deepcopy(structure_data)

    def __str__(self) -> str:
        return self._sentence

    @property
    def sentence(self) -> str:
        return self._sentence

    @property
    def structure_data(self) -> list:
        return copy.deepcopy(self._structure_data)

    def get(self, omit_empty_strings=False) -> list:
        structure_data = copy.deepcopy(self._structure_data)
        if omit_empty_strings == True:
            structure_data = [s for s in structure_data if s[0] != ""]
        return structure_data

    def shrink_analysis_results(self, bottom_hierarchy) -> Self:
        structure_data = []
        join_next_time_with_previous = False
        for s in copy.deepcopy(self._structure_data):
            if join_next_time_with_previous == True:
                structure_data[-1][0] += s[0]
                join_next_time_with_previous = False
            elif s[1] <= bottom_hierarchy:
                structure_data.append(s)
            else:
                structure_data[-1][0] += s[0]
                join_next_time_with_previous = True
        return SentenceStructureInformation(self._sentence, structure_data)


def analyze_sentence(sentence, delimiter, delimiter_handling_mode=DelimiterHandlingMode.ADDITIONAL_TO_AROUND, consider_escaping=False) -> SentenceStructureInformation:
    def prepare_pattern(template, delimiter) -> str:
        pattern = ""
        if type(delimiter) == tuple:
            delimiter = [delimiter]
        for d in delimiter:
            pattern += "|" + template.format(re.escape(d[0]), re.escape(d[1]))
        pattern = "(" + pattern.lstrip("|") + ")"
        return pattern

    def hierarchize_sentence(pattern, sentence, delimiter_handling_mode, hierarchy) -> list:
        split_sentences_1 = re.split(pattern, sentence)
        if len(split_sentences_1) == 1:
            split_sentences_1.append(hierarchy + 1)
            return [split_sentences_1]
        else:
            split_sentences_2 = []
            another_hierarchy = False
            character_append_in_string_first = None
            for part in split_sentences_1:
                if another_hierarchy == True:
                    split_sentences_temp = hierarchize_sentence(pattern, part[1:-1], delimiter_handling_mode, hierarchy + 1)
                    if delimiter_handling_mode == DelimiterHandlingMode.ADDITIONAL_TO_AROUND:
                        split_sentences_2[-1][0] += part[0]
                        character_append_in_string_first = part[-1]
                    elif delimiter_handling_mode == DelimiterHandlingMode.ADDITIONAL_TO_BODY:
                        split_sentences_temp[0][0] = split_sentences_temp[0][0] + part[0]
                        split_sentences_temp[-1][0] += part[-1]
                    split_sentences_2 += split_sentences_temp
                else:
                    split_sentences_temp = hierarchize_sentence(pattern, part, delimiter_handling_mode, hierarchy)
                    if character_append_in_string_first is not None:
                        split_sentences_temp[0][0] = character_append_in_string_first + split_sentences_temp[0][0]
                        character_append_in_string_first = None
                    split_sentences_2 += split_sentences_temp
                another_hierarchy = another_hierarchy == False
            if character_append_in_string_first is not None:
                split_sentences_2[-1][0] = character_append_in_string_first + split_sentences_2[-1][0]
            return split_sentences_2

    if consider_escaping == True:
        template = "{0}.*(?<!\\\\){1}"
    else:
        template = "{0}.*{1}"
    pattern = prepare_pattern(template, delimiter)
    structure_data = hierarchize_sentence(pattern, sentence, delimiter_handling_mode, -1)
    return SentenceStructureInformation(sentence, structure_data)


def ab_to_ba(data) -> list:
    return [d[::-1] for d in data]


def ab_to_a(data) -> list:
    return [d[0] for d in data]


def ab_to_b(data) -> list:
    return [d[1] for d in data]


def a_b_to_ab(a, b) -> list:
    if len(a) != len(b):
        raise Exception("The number of elements in list a and list b do not match.")
    return [list(d) for d in zip(a, b)]