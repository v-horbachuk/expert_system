#!/usr/bin/env python
from src.algorithm import solve
from src import read, validate as validate
from src.strings import QueryString, InitFactString, BadString
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
from termcolor import colored


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
    exit(colored(e, 'red'))

markings_to_replace = list()
markings_to_replace.append((markings.get('imply'), markings.get('imply_new')))
markings_to_replace.append((markings.get('bicondition'), markings.get('bicondition_new')))

try:
    validate.check_conditions_in_trimed_data(trimmed_data, markings.get('init_fact'), markings.get('quotation'),
                                             markings.get('imply'), markings.get('bicondition'))
except BadConditionError as e:
    exit(colored(e, 'red'))

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

solve(goal_facts=goal_facts, known_facts=known_facts, equations=equations)

print(colored("These lines were used during algorithm execution:", 'yellow'))
rules = list()
bad_strings = list()
for string in strings:
    if isinstance(string, QueryString):
        print(colored(f"Goal facts: {string}", 'magenta'))
    elif isinstance(string, InitFactString):
        print(colored(f"Init facts: {string}", 'magenta'))
    elif isinstance(string, BadString):
        bad_strings.append(string)
    else:
        rules.append(string)

if rules:
    for rule in rules: print(colored(f"Rule: {rule}", 'green'))

if bad_strings:
    print(colored("\nThese lines are bad:", 'yellow'))
    for bad in bad_strings: print(colored(f"Bad line: {bad}", 'red'))

for goal in goal_facts:
    if not goal.value:
        print(colored(f"\n{goal.name}", 'cyan'), "is", colored(f"{goal.value}", 'red'))
    else:
        print(colored(f"\n{goal.name}", 'cyan'), "is", colored(f"{goal.value}", 'green'))
