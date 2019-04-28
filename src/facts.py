

class Fact:

    def __init__(self, name, value=False):
        self.__set_name(name)
        self.value = value

    def __hash__(self):
        return hash(self.name)

    def __or__(self, other):
        return self.value or other.value

    def __and__(self, other):
        return self.value and other.value

    def __xor__(self, other):
        return self.value ^ other.value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __bool__(self):
        return self.value

    def __set_name(self, data):
        self._name = data

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_goal(self):
        return False

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, data: bool):
        self._value = data


class Goal(Fact):

    @property
    def is_goal(self):
        return True
