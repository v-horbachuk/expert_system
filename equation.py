from strings import String
from facts import Fact
from custom_utils import markings


class RightEquationPart:
    def __init__(self, string, facts):
        self.string = string
        self.facts = facts
        self.executable_string = self.get_operands_for_eval(string.data)

    def __str__(self):
        return self.eval_string

    def __contains__(self, item):
        if isinstance(item, Fact):
            if item in self.facts:
                return True
            return False
        return NotImplemented

    @property
    def facts(self):
        return self._facts

    @facts.setter
    def facts(self, value):
        if not self.string:
            raise ValueError('Rules must be positioned before facts')
        real_facts = list()
        for fact in value:
            if fact in self.string:
                real_facts.append(fact)
        self._facts = real_facts

    @property
    def eval_string(self):
        comparision_dict = {fact.name: str(fact) for fact in self.facts}
        facts_line = self.executable_string
        for name, fact_str in comparision_dict.items():
            facts_line = facts_line.replace(name, '{' + name + '}')
        facts_line = facts_line.format(**comparision_dict)
        return facts_line

    @property
    def result(self):
        return eval(str(self))

    @property
    def known_sum(self):
        known_facts = [fact for fact in self.facts if fact.value is True]
        return len(known_facts)

    @staticmethod
    def get_operands_for_eval(string):
        rules = {
            "imply_new": ">",
            "or": "|",
            "xor": "^",
            "left_bracket": "(",
            "right_bracket": ")",
            "not": "!",
            "and": "+"
        }

        data_for_eval = {
            'imply_new': ' > ',
            'or': ' or ',
            'xor': ' ^ ',
            'left_bracket': ' ( ',
            'right_bracket': ' ) ',
            'not': ' not ',
            'and': ' and ',
        }

        for name, field in rules.items():
            replace_to = data_for_eval.get(name)
            string = string.replace(rules[name], replace_to)
        return string


class LeftEquationPart:
    def __init__(self, string, facts):
        self.string = string
        self.facts = facts
        self.executable_string = self.get_operands_for_eval(string.data)

    def __str__(self):
        return self.eval_string

    def __contains__(self, item):
        if isinstance(item, Fact):
            if item in self.facts:
                return True
            return False
        return NotImplemented

    @property
    def facts(self):
        return self._facts

    @facts.setter
    def facts(self, value):
        if not self.string:
            raise ValueError('Rules must be positioned before facts')
        real_facts = list()
        for fact in value:
            if fact in self.string:
                real_facts.append(fact)
        self._facts = real_facts

    @property
    def eval_string(self):
        comparision_dict = {fact.name: str(fact) for fact in self.facts}
        facts_string = self.executable_string
        for name, fact_str in comparision_dict.items():
            facts_string = facts_string.replace(name, '{' + name + '}')
        facts_string = facts_string.format(**comparision_dict)
        return facts_string

    @property
    def result(self):
        return eval(str(self))

    @property
    def known_sum(self):
        known_facts = [fact for fact in self.facts if fact.value is True]
        return len(known_facts)

    @staticmethod
    def get_operands_for_eval(string):
        rules = {
            "imply_new": ">",
            "or": "|",
            "xor": "^",
            "left_bracket": "(",
            "right_bracket": ")",
            "not": "!",
            "and": "+"
        }

        data_for_eval = {
            'imply_new': ' > ',
            'or': ' or ',
            'xor': ' ^ ',
            'left_bracket': ' ( ',
            'right_bracket': ' ) ',
            'not': ' not ',
            'and': ' and ',
        }

        for name, field in rules.items():
            replace_to = data_for_eval.get(name)
            string = string.replace(rules[name], replace_to)
        return string


class Equation:

    def __init__(self, line, facts):
        self.line = line
        left_part, right_part = line.data.split(markings.get('imply_new'))

        left_part_string = String(left_part)
        right_part_string = String(right_part)

        left_part_facts = list()
        for fact in facts:
            if fact in left_part_string:
                left_part_facts.append(fact)

        right_part_facts = list()
        for fact in facts:
            if fact in right_part_string:
                right_part_facts.append(fact)

        self.left_part = LeftEquationPart(left_part_string, left_part_facts)
        self.right_part = RightEquationPart(right_part_string, right_part_facts)

    def __str__(self):
        return repr(self)

    def __contains__(self, item):
        if isinstance(item, Fact):
            in_left_part = item in self.left_part
            in_right_part = item in self.right_part
            if in_left_part or in_right_part:
                return True
            return False
        return NotImplemented
