def parse_rules(rules):
    parsed_rules = []
    with open(rules, 'r') as file:
        for line in file:
            line = line.strip()
            if "THEN" in line:
                condition_part, conclusion = line.split("THEN")
                condition_part = condition_part.replace("IF", "").strip()
                conclusion = conclusion.strip()

                if " AND " in condition_part:
                    operator = "AND"
                    conditions = [c.strip() for c in condition_part.split(" AND ")]
                elif " OR " in condition_part:
                    operator = "OR"
                    conditions = [c.strip() for c in condition_part.split(" OR ")]
                else:
                    operator = "AND"
                    conditions = [condition_part.strip()]

                parsed_rules.append({
                    "conditions": conditions,
                    "operator": operator,
                    "conclusion": conclusion
                })
    return parsed_rules


def parse_facts(facts):
    parsed_facts = set()
    parsed_variables = {}
    
    with open(facts, 'r') as file:
        for line in file:
            fact = line.strip()
            if fact:
                if "=" in fact and not any(op in fact for op in [">=", "<=", "!=", "=="]):
                    var_name, var_value = fact.split("=", 1)
                    var_name = var_name.strip()
                    var_value = var_value.strip()
                    
                    try:
                        var_value = float(var_value)
                        if var_value.is_integer():
                            var_value = int(var_value)
                    except ValueError:
                        pass
                    
                    parsed_variables[var_name] = var_value
                    parsed_facts.add(fact)
                else:
                    parsed_facts.add(fact)
    
    return parsed_facts, parsed_variables


def evaluate_condition(condition, facts, variables):
    if condition in facts:
        return True
    
    operators = [">=", "<=", "!=", "==", ">", "<"]
    for op in operators:
        if op in condition:
            left, right = condition.split(op, 1)
            left = left.strip()
            right = right.strip()
            
            left_val = variables.get(left, left)
            right_val = variables.get(right, right)
            
            try:
                if isinstance(left_val, str) and left_val not in variables:
                    left_val = float(left_val)
                    if left_val.is_integer():
                        left_val = int(left_val)
            except ValueError:
                pass
                
            try:
                if isinstance(right_val, str) and right_val not in variables:
                    right_val = float(right_val)
                    if right_val.is_integer():
                        right_val = int(right_val)
            except ValueError:
                pass
            
            if op == ">=":
                return left_val >= right_val
            elif op == "<=":
                return left_val <= right_val
            elif op == "!=":
                return left_val != right_val
            elif op == "==":
                return left_val == right_val
            elif op == ">":
                return left_val > right_val
            elif op == "<":
                return left_val < right_val
    
    return False


def backward_chaining(goal, rules, facts, variables, visited=None, depth=0, cycle_counter=None):
    if visited is None:
        visited = set()
    if cycle_counter is None:
        cycle_counter = [0]
    
    cycle_counter[0] += 1
    current_cycle = cycle_counter[0]
    
    indent = "  " * depth
    print(f"\n{indent}[Cycle {current_cycle}] Trying to prove: {goal}")
    
    if goal in facts:
        print(f"{indent}[Cycle {current_cycle}] ✓ Goal '{goal}' is already a known fact.")
        return True, facts, variables
    
    if any(op in goal for op in [">=", "<=", "!=", "==", ">", "<"]):
        result = evaluate_condition(goal, facts, variables)
        if result:
            print(f"{indent}[Cycle {current_cycle}] ✓ Condition '{goal}' evaluates to True.")
            return True, facts, variables
        else:
            print(f"{indent}[Cycle {current_cycle}] ✗ Condition '{goal}' evaluates to False.")
    
    if goal in visited:
        print(f"{indent}[Cycle {current_cycle}] ✗ Goal '{goal}' was already visited (cycle detected).")
        return False, facts, variables
    
    visited.add(goal)
    
    relevant_rules = [rule for rule in rules if rule["conclusion"] == goal]
    
    if not relevant_rules:
        print(f"{indent}[Cycle {current_cycle}] ✗ No rules found with conclusion '{goal}'.")
        return False, facts, variables
    
    print(f"{indent}[Cycle {current_cycle}] Found {len(relevant_rules)} rules with conclusion '{goal}'.")
    
    for i, rule in enumerate(relevant_rules):
        print(f"\n{indent}[Cycle {current_cycle}] Trying rule {i+1}: IF {' ' + rule['operator'] + ' '.join(rule['conditions'])} THEN {rule['conclusion']}")
        
        can_satisfy = True
        new_facts = facts.copy()
        new_variables = variables.copy()
        
        if rule["operator"] == "AND":
            for condition in rule["conditions"]:
                print(f"{indent}  [Cycle {current_cycle}] Checking AND condition: {condition}")
                condition_satisfied, new_facts, new_variables = backward_chaining(condition, rules, new_facts, new_variables, visited.copy(), depth + 1, cycle_counter)
                if not condition_satisfied:
                    print(f"{indent}  [Cycle {current_cycle}] ✗ Condition '{condition}' cannot be satisfied.")
                    can_satisfy = False
                    break
                else:
                    print(f"{indent}  [Cycle {current_cycle}] ✓ Condition '{condition}' is satisfied.")
        else:
            can_satisfy = False
            for condition in rule["conditions"]:
                print(f"{indent}  [Cycle {current_cycle}] Checking OR condition: {condition}")
                condition_satisfied, condition_facts, condition_variables = backward_chaining(condition, rules, new_facts, new_variables, visited.copy(), depth + 1, cycle_counter)
                if condition_satisfied:
                    print(f"{indent}  [Cycle {current_cycle}] ✓ Condition '{condition}' is satisfied.")
                    can_satisfy = True
                    new_facts = condition_facts
                    new_variables = condition_variables
                    break
                else:
                    print(f"{indent}  [Cycle {current_cycle}] ✗ Condition '{condition}' cannot be satisfied, trying next OR condition if available.")
        
        if can_satisfy:
            new_facts.add(goal)
            print(f"\n{indent}[Cycle {current_cycle}] ✓ All conditions for rule {i+1} are satisfied. Adding '{goal}' to facts.")
            
            if "=" in goal and not any(op in goal for op in [">=", "<=", "!=", "=="]):
                var_name, var_value = goal.split("=", 1)
                var_name = var_name.strip()
                var_value = var_value.strip()
                
                try:
                    var_value = float(var_value)
                    if var_value.is_integer():
                        var_value = int(var_value)
                except ValueError:
                    pass
                
                new_variables[var_name] = var_value
            
            print(f"{indent}[Cycle {current_cycle}] Current facts:")
            print_facts(new_facts, indent + "  ")
            return True, new_facts, new_variables
    
    print(f"\n{indent}[Cycle {current_cycle}] ✗ No rules could satisfy the goal '{goal}'.")
    return False, facts, variables


def print_facts(facts, indent=""):
    for fact in sorted(facts):
        print(f"{indent}- {fact}")


def print_variables(variables, indent=""):
    for var_name, var_value in sorted(variables.items()):
        print(f"{indent}- {var_name} = {var_value}")


if __name__ == "__main__":
    rules = parse_rules("rules.txt")
    facts, variables = parse_facts("facts.txt")

    print("=" * 50)
    print("PRODUCTION SYSTEM - BACKWARD CHAINING")
    print("=" * 50)
    
    print("\nParsed Rules:")
    for i, rule in enumerate(rules):
        print(f"Rule {i+1}:")
        print(f"  IF {' ' + rule['operator'] + ' '.join(rule['conditions'])}")
        print(f"  THEN {rule['conclusion']}")
        print("-" * 40)

    print("\nInitial Facts:")
    print_facts(facts)
    
    goal = "citrus_fruit"
    print("\n" + "="*50)
    print(f"STARTING BACKWARD CHAINING with goal: {goal}")
    print("="*50)
    goal_achieved, resulting_facts, resulting_variables = backward_chaining(goal, rules, facts.copy(), variables.copy())
    
    print("\n" + "="*50)
    print("BACKWARD CHAINING RESULT")
    print("="*50)
    if goal_achieved:
        print(f"\n✓ Goal '{goal}' CAN be achieved!")
        
        new_facts = resulting_facts - facts
        if new_facts:
            print("\nNew facts derived during backward chaining:")
            for fact in new_facts:
                print(f"- {fact}")
        else:
            print("\nNo new facts were derived during backward chaining.")
    else:
        print(f"\n✗ Goal '{goal}' CANNOT be achieved with the given rules and facts.")
