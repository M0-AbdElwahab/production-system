def parse_rules(rules):
    ruless = []
    with open(rules, 'r') as file:
        for line in file:
            if "THEN" in line:
                parts = line.strip().split("THEN")
                if len(parts) == 2:
                    condition = parts[0].strip()
                    conclusion = parts[1].strip()
                    ruless.append((condition, conclusion))
    return ruless

def parse_facts(facts):
    factss = set()
    with open(facts, 'r') as file:
        for line in file:
            fact = line.strip()
            if fact:
                factss.add(fact)
    return factss

if __name__ == "__main__":
    rules = parse_rules("rules.txt")
    facts = parse_facts("facts.txt")

    print("Parsed Rules:")
    for r in rules:
        print(f"IF {r[0]} THEN {r[1]}")

    print("\nParsed Facts:")
    for f in facts:
        print(f)
