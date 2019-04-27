from custom_utils import markings
import validate as validate
from negative_sign_handle import wrap_negative_facts_in_brackets


class String:

    def __init__(self, string):
        self.raw_data = string
        self.data = string

    @property
    def string_type(self):
        return 'string'

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def __contains__(self, obj):
        if isinstance(obj, str):
            return obj in self.data
        return obj.name in self.data

    @property
    def is_valid(self):
        return True

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, string):
        self._raw_data = self._wrap_negatives(string)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, string):
        self._data = self._wrap_negatives(string)

    def _wrap_negatives(self, string):
        wrapped_string = wrap_negative_facts_in_brackets(string)
        return wrapped_string


class BadString(String):
    @property
    def is_valid(self):
        return False

    @property
    def string_type(self):
        return 'bad_string'


class RuleString(String):
    @property
    def string_type(self):
        return 'rule_string'


class BiconditionRuleString(RuleString):
    @property
    def string_type(self):
        return 'bicondition_string'


class QueryString(String):

    @property
    def string_type(self):
        return 'query_string'

    def __init__(self, string):
        super().__init__(string)
        self.data = string[1:]

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.raw_data)


class InitFactString(String):

    @property
    def string_type(self):
        return 'initial_fact_string'

    def __init__(self, string):
        super().__init__(string)
        self.data = string[1:]

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.raw_data)


def string_type_define(string):
    if validate.define_query_or_fact_string(string, markings.get('quotation')):
        return QueryString(string)
    if validate.define_query_or_fact_string(string, markings.get('init_fact')):
        return InitFactString(string)
    if validate.define_rule_string(string):
        if markings.get('imply_new') in string:
            return RuleString(string)
        if markings.get('bicondition_new') in string:
            return BiconditionRuleString(string)
    return BadString(string)
