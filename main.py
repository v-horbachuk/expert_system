#!/usr/bin/env python
from src.algorithm import solve
from src.output import print_transformed_validated_strings, bold_red, print_goals
from src import read, validate as validate
from src.exceptions import BadConditionError
from src.get_strings import pop_bad_strings, \
    validate_initial_fact_strings, \
    validate_query_strings, \
    bicondition_strings_to_rule_strings, \
    extract_facts_from_strings
from src.strings import string_type_define, RuleString
from src.facts import Fact, Goal
from src.equation import Equation
from src.custom_utils import markings
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description='Expert System.')
    parser.add_argument("-f",
                        "--file",
                        required=True,
                        action='store',
                        help="file with rules and facts")
    args = parser.parse_args()
    return args


args = parse_args()
try:
    trimmed_data = read.read_file(args.file)
except FileNotFoundError as e:
    exit(bold_red(e))

markings_to_replace = list()
markings_to_replace.append((markings.get('imply'), markings.get('imply_new')))
markings_to_replace.append((markings.get('bicondition'), markings.get('bicondition_new')))

try:
    validate.check_conditions_in_trimed_data(trimmed_data, markings.get('init_fact'), markings.get('quotation'),
                                             markings.get('imply'), markings.get('bicondition'))
except BadConditionError as e:
    exit(bold_red(e))

prepared_data = validate.markings_replace(trimmed_data, markings_to_replace)
strings = list()
for string in prepared_data:
    strings.append(string_type_define(string))
strings = set(strings)

valid_strings = pop_bad_strings(strings)
try:
    validate_initial_fact_strings(strings)
except ValueError as e:
    exit(e)
try:
    validate_query_strings(strings)
except ValueError as e:
    exit(e)

bad_strings = strings.difference(valid_strings)
valid_strings = bicondition_strings_to_rule_strings(valid_strings, '>', '<')
raw_facts = extract_facts_from_strings(valid_strings)
initial_string = next(string for string in valid_strings if string.string_type == 'initial_fact_string')
query_string = next(string for string in valid_strings if string.string_type == 'query_string')

facts = list()
for raw_fact in raw_facts:
    fact = Goal(name=raw_fact) if raw_fact in query_string.data else Fact(name=raw_fact)
    fact.value = True if raw_fact in initial_string.data else False
    facts.append(fact)

known_facts = list()
for fact in facts:
    if fact.value is True:
        known_facts.append(fact)

goal_facts = list()
for fact in facts:
    if fact.is_goal is True:
        goal_facts.append(fact)

equations = list()
for string in valid_strings:
    if isinstance(string, RuleString):
        string_facts = list()
        for fact in facts:
            if fact in string:
                string_facts.append(fact)
        equations.append(Equation(string, string_facts))
expressions = sorted(equations, key=lambda equation: equation.left_part.known_sum, reverse=True)

try:
    solve(goal_facts=goal_facts, known_facts=known_facts, equations=equations)
except (SyntaxError, NameError):
    exit(bold_red('Bad file or data'))

print_transformed_validated_strings(strings)
print_goals(goal_facts)
