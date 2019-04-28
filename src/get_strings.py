import re
from src.strings import RuleString


def is_bad_string(string, bad_pattern=None):
    if not bad_pattern:
        return string.string_type == 'bad_string'
    return False


def pop_bad_strings(strings):
    good_strings = strings.copy()
    for string in strings:
        if is_bad_string(string):
            good_strings.discard(string)
    return good_strings


def validate_initial_fact_strings(strings):
    counter = 0
    for string in strings:
        if string.string_type == 'initial_fact_string':
            counter += 1
    if counter != 1:
        raise ValueError('There should be only one initial fact string')


def validate_query_strings(strings):
    counter = 0
    for string in strings:
        if string.string_type == 'query_string':
            counter += 1
    if counter != 1:
        raise ValueError('There should be only one query string')


def bicondition_strings_to_rule_strings(strings, implies_sub, bicodition_sub):
    tmp_strings = strings.copy()
    for string in tmp_strings:
        if string.string_type == 'bicondition_string':
            strings.remove(string)
            new_str = string.data.replace(bicodition_sub, implies_sub)
            strings.add(RuleString(new_str))
            reversed_new_str_parts = reversed(new_str.split(implies_sub))
            reversed_new_str = f'{implies_sub}'.join(reversed_new_str_parts)
            strings.add(RuleString(reversed_new_str))
    return strings


def extract_facts_from_strings(strings_set):
    extracted_facts = []
    for string in strings_set:
        string_facts = re.findall(r'\w', string.data)
        extracted_facts.extend(string_facts)
    extracted_facts = set(extracted_facts)
    return extracted_facts
