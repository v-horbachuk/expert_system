
recursion_list = []


def solve(goal_facts, known_facts, equations):
    for goal in goal_facts:
        backward_chain(goal, known_facts, equations)


def backward_chain(goal, known_facts, equations):
    if goal not in known_facts:
        # get expressions where goal is in conclusion
        # goal_expressions = ExpressionList(expr for expr in expressions if goal in expr.conclusion)
        goal_equations = list()
        for equation in equations:
            if goal in equation.right_part:
                goal_equations.append(equation)
        if not goal_equations:
            known_facts.append(goal)
        for equation in goal_equations:
            left_part_facts = equation.left_part.facts
            for fact in left_part_facts:
                if fact not in left_part_facts: # prevent infinite recursion
                    backward_chain(fact, known_facts, equations)
            if goal not in known_facts: # Was added to prevent extra recursion
                solver(equation, known_facts, equations)


def solver(equation, known_facts, equations):
    for fact in equation.left_part.facts:
        if fact in equation.right_part.facts or fact in recursion_list:
            continue
        else:
            recursion_list.append(fact)
            backward_chain(fact, known_facts, equations)
    result = eval(equation.left_part.eval_string)
    for fact in equation.right_part.facts:
        if fact not in known_facts and fact not in equation.left_part.facts:
            if result != eval(equation.right_part.eval_string):
                fact.value = not fact.value
            known_facts.append(fact)
