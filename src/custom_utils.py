import string

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
