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


def forward_chaining(rules, facts, variables):
    new_facts = set(facts)
    new_variables = dict(variables)
    added = True
    cycle = 0

    while added:
        added = False
        cycle += 1
        print(f"\n[Cycle {cycle}] Forward chaining cycle started.")
        
        for rule in rules:
            conditions_met = []

            for condition in rule["conditions"]:
                if condition in new_facts or evaluate_condition(condition, new_facts, new_variables):
                    conditions_met.append(True)
                else:
                    conditions_met.append(False)

            if rule["operator"] == "AND" and all(conditions_met):
                conclusion = rule["conclusion"]
                if conclusion not in new_facts:
                    new_facts.add(conclusion)
                    print(f"✓ Rule fired: {rule} ➔ Added new fact: {conclusion}")
                    added = True

                    
                    if "=" in conclusion and not any(op in conclusion for op in [">=", "<=", "!=", "=="]):
                        var_name, var_value = conclusion.split("=", 1)
                        var_name = var_name.strip()
                        var_value = var_value.strip()
                        
                        try:
                            var_value = float(var_value)
                            if var_value.is_integer():
                                var_value = int(var_value)
                        except ValueError:
                            pass
                        
                        new_variables[var_name] = var_value

            elif rule["operator"] == "OR" and any(conditions_met):
                conclusion = rule["conclusion"]
                if conclusion not in new_facts:
                    new_facts.add(conclusion)
                    print(f"✓ Rule fired: {rule} ➔ Added new fact: {conclusion}")
                    added = True

    return new_facts, new_variables


    


def print_facts(facts, indent=""):
    for fact in sorted(facts):
        print(f"{indent}- {fact}")


def print_variables(variables, indent=""):
    for var_name, var_value in sorted(variables.items()):
        print(f"{indent}- {var_name} = {var_value}")


if __name__ == "__main__":
    rules = parse_rules("rules.txt")
    facts, variables = parse_facts("facts.txt")

print("\n" + "="*50)
print("STARTING FORWARD CHAINING")
print("="*50)

resulting_facts_fc, resulting_variables_fc = forward_chaining(rules, facts.copy(), variables.copy())

print("\n" + "="*50)
print("FORWARD CHAINING RESULT")
print("="*50)

print("\nFinal Facts:")
print_facts(resulting_facts_fc)

if "citrus_fruit" in resulting_facts_fc:
    print("\n The fruit IS a citrus fruit! ")
else:
    print("\n The fruit is NOT a citrus fruit. ")

    


    
    