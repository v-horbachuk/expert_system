import string
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description='Expert System.')
    parser.add_argument("-c",
                        "--config",
                        metavar="file",
                        default="operators.yaml",
                        help="Path to *.yaml file with symbols configuration")
    parser.add_argument("-f",
                        "--file",
                        required=True,
                        action='store',
                        help="file with rules and facts")
    args = parser.parse_args()
    return args


markings = {
    "imply": "=>",
    "imply_new": ">",
    "bicondition": "<=>",
    "bicondition_new": "<",
    "or": "|",
    "xor": "^",
    "left_bracket": "(",
    "right_bracket": ")",
    "not": "!",
    "and": "+",
    "init_fact": "=",
    "quotation": "?"
}

facts = set(string.ascii_uppercase)
