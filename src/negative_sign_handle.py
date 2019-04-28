def wrap_negative_fact(symbols, i, left='(', right=')', op_not='!'):
    try:
        char_before = symbols[i - 1]
    except IndexError:
        i += 1
        return i
    if char_before != op_not:
        i += 1
        return i
    try:
        symbols.insert(i - 1, left)
    except IndexError:
        symbols.insert(0, left)
    try:
        symbols.insert(i + 2, right)
    except IndexError:
        symbols.insert(len(symbols), right)
    i += 3
    return i


def wrap_negative_comprehesion(symbols, i, left='(', right=')', op_not='!'):
    left_index = i
    right_index = i
    brackets_count = 0
    changed = False
    for j, char in enumerate(symbols[i:]):
        if changed and brackets_count == 0:
            continue
        if char == left:
            brackets_count += 1
            changed = True
        elif char == right:
            brackets_count -= 1
            changed = True
            right_index = j + i
    else:
        if changed and brackets_count == 0:
            symbols.insert(left_index, left)
            symbols.insert(right_index + 1, right)
            i += 1
    return i


def wrap_negative_facts_in_brackets(line, left='(', right=')', op_not='!'):
    symbols = list(line)
    i = 0
    while i < len(symbols):
        if symbols[i].isupper():
            i = wrap_negative_fact(symbols, i)
        elif len(symbols) > i + 1 and symbols[i] == op_not and symbols[i + 1] == left:
            i = wrap_negative_comprehesion(symbols, i)
            i += 1
        else:
            i += 1
    wrapped_line = ''.join(symbols)
    return wrapped_line