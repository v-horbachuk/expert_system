from strings import QueryString, InitFactString

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BOLD_RED = FAIL + BOLD


def bold_red(text):
    return f'{BOLD_RED}{text}{ENDC}'


def print_goals(goals):
    for goal in goals:
        name_color = OKBLUE + BOLD
        val_color = OKGREEN if goal.value else FAIL
        print(f'{name_color}{goal.name}{ENDC} is {val_color}{goal.value}{ENDC}')


def print_transformed_validated_strings(strings):
    print(f'{BOLD}Lines will be used in computation{ENDC} (red lines will be ommitted during computation):')
    initial_facts_string = ''
    goal_strings = ''
    other_strings = []
    for string in strings:
        if isinstance(string, QueryString):
            goal_strings = string
        elif isinstance(string, InitFactString):
            initial_facts_string = string
        else:
            other_strings.append(string)
    for line in other_strings:
        if line.is_valid:
            print(f'{OKGREEN}{line.raw_data}{ENDC}')
        else:
            print(bold_red(line.raw_data))
    print(f'{BOLD}Initial facts: {initial_facts_string.data}{ENDC}')
    print(f'{BOLD}Goals are: {goal_strings.data}{ENDC}')
