from src.exceptions import BadConditionError
from src.custom_utils import markings, facts


#---------------------------- Condition validation-------------------------------


def check_conditions_in_trimed_data(trimmed_data, init_fact, quotation, imply, bicondition):
    """Checks =>, <=> for each string in trimmed data"""
    conditions = sorted([imply, bicondition], key=lambda tup: len(tup), reverse=True)
    for string in trimmed_data:
        if string.startswith((quotation, init_fact)):
            continue
        entry = 0
        for condition in conditions:
            if entry == 1:
                break
            entry += string.count(condition)
        if entry == 0:
            raise BadConditionError(string=string)


def markings_replace(trimmed_data, markings):
    """Replace =>, <=> to >, < in each string in trimmed data"""
    replaced_data = trimmed_data.copy()
    markings = list(sorted(markings, key=lambda x: len(x[0]), reverse=True))
    for marking, sign in markings:
        for i, string in enumerate(replaced_data):
            if marking in string:
                replaced_data[i] = string.replace(marking, sign)
    return replaced_data


#---------------------------- String validation----------------------------------
# = validate_rule + line_begin + line_end + operator_duplication
def check_rule_valid(string):
    if markings.get('imply_new') in string:
        splitter = markings.get('imply_new')
    else:
        splitter = markings.get('bicondition_new')
    parts_list = string.split(splitter, 1)
    is_valid = list()
    for part in parts_list:
        # stripped_data = part.lstrip() ???????????? => clean white spaces Todo - test
        if part.startswith((markings.get('left_bracket'), *facts, markings.get('not'))):
            is_valid.append(True)
        else:
            is_valid.append(False)
        if part.endswith((markings.get('right_bracket'), *facts)):
            is_valid.append(True)
        else:
            is_valid.append(False)
        # regexp = re.compile(f'[{string.whitespace}]+')
        # clean_string = regexp.sub(r'', string)
        duplicates = list()
        for element in (markings.get('and'), markings.get('or'), markings.get('xor')):
            element = element * 2
            duplicates.append(element)
        for duplicate in duplicates:
            if duplicate in string:    #change for clean_string if regex used
                is_valid.append(False)
        is_valid.append(True)
    if False in is_valid:
        return False
    return True


# = can_be_rule
def check_condition(string):
    if markings.get('bicondition_new') in string:
        bicondition = True
    else:
        bicondition = False

    if markings.get('imply_new') in string:
        imply = True
    else:
        imply = False

    if string.count(markings.get('bicondition_new')) + string.count(markings.get('imply_new')) == 1:
        valid = True
    else:
        valid = False
    result = (bicondition or imply) and valid
    return result


def define_rule_string(string):
    conditions = [markings.get('left_bracket'), markings.get('right_bracket'), markings.get('not'),
                  markings.get('and'), markings.get('or'), markings.get('xor'), markings.get('imply_new'),
                  markings.get('bicondition_new')]

    for char in string:
        if char not in conditions and char not in facts:
            return False
    #TODO test to change in to is
    brackets = []
    open_bracket = [markings.get('left_bracket')]
    close_bracket = [markings.get('right_bracket')]
    for elem in string:
        if elem in open_bracket:
            brackets.append(elem)
        elif elem in close_bracket:
            pos = close_bracket.index(elem)
            if (len(brackets) > 0) and (open_bracket[pos] == brackets[len(brackets) - 1]):
                brackets.pop()
            else:
                return False
    if len(brackets) == 0:
        pass
    if check_condition(string):
        return check_rule_valid(string)
    else:
        return False


def define_query_or_fact_string(string, marking):
    marking_from_string, *facts = string
    facts = ''.join(facts)
    letter_or_empty = facts.isalpha() or facts == ''
    if marking_from_string != marking or not letter_or_empty:
        return False
    else:
        return True
