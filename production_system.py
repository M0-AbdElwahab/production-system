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
    with open(facts, 'r') as file:
        for line in file:
            fact = line.strip()
            if fact:
                parsed_facts.add(fact)
    return parsed_facts


if __name__ == "__main__":
    rules = parse_rules("rules.txt")
    facts = parse_facts("facts.txt")

    print("Parsed Rules:")
    for rule in rules:
        print(f"Operator: {rule['operator']}")
        print(f"Conditions: {rule['conditions']}")
        print(f"Conclusion: {rule['conclusion']}")
        print("-" * 40)

    print("\nParsed Facts:")
    for fact in facts:
        print(fact)
