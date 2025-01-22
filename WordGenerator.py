import itertools

class Node:
    def __init__(self, kind, children=None, value=None):
        self.kind = kind
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        if self.kind == 'char':
            return f"CHAR({self.value!r})"
        elif self.kind == 'concat':
            return "CONCAT(" + ",".join(repr(c) for c in self.children) + ")"
        elif self.kind == 'alt':
            return "ALT(" + ",".join(repr(c) for c in self.children) + ")"
        elif self.kind == 'star':
            return f"STAR({repr(self.children[0])})"
        return f"Node({self.kind}, {self.children}, {self.value!r})"


def parse_regex(regex):
    index = 0
    n = len(regex)

    def peek():
        return regex[index] if index < n else None

    def consume():
        nonlocal index
        ch = peek()
        index += 1
        return ch

    def parse_expression():
        node = parse_concatenation()
        while peek() == '+':
            consume() 
            right = parse_concatenation()
            if node.kind == 'alt':
                node.children.append(right)
            else:
                node = Node('alt', [node, right])
        return node

    def parse_concatenation():
        factors = []
        while True:
            ch = peek()
            if ch is None or ch in (')', '+'):
                break
            factors.append(parse_factor())
        if not factors:
            return Node('char', value="")
        if len(factors) == 1:
            return factors[0]
        return Node('concat', factors)

    def parse_factor():
        """
        factor := base ('*')?
        """
        base_node = parse_base()
        while peek() == '*':
            consume()
            base_node = Node('star', [base_node])
        return base_node

    def parse_base():
        """
        base := '(' expression ')' | single_character | 'ɛ'
        """
        ch = peek()
        if ch is None:
            return Node('char', value="")

        if ch == '(':
            consume()  # skip '('
            subexpr = parse_expression()
            if peek() == ')':
                consume()  # skip ')'
            else:
                raise ValueError("Missing closing parenthesis")
            return subexpr

        if ch in (')', '+', '*'):
            raise ValueError(f"Unexpected character '{ch}' in parse_base")

        consume()
        if ch == 'ɛ':
            ch = "" 
        return Node('char', value=ch)

    root = parse_expression()

    if index < n:
        raise ValueError(f"Extra unparsed characters: {regex[index:]}")
    return root


def generate_from_tree(node, max_repetitions=3):
    if node.kind == 'char':
        yield node.value
        return

    elif node.kind == 'star':
        child = node.children[0]
        seen = set()
        child_strings = list(generate_from_tree(child, max_repetitions))
        for count in range(max_repetitions + 1):
            if count == 0:
                if "" not in seen:
                    seen.add("")
                    yield ""
            else:
                for combo in itertools.product(child_strings, repeat=count):
                    out = "".join(combo)
                    if out not in seen:
                        seen.add(out)
                        yield out

    elif node.kind == 'alt':
        seen = set()
        for c in node.children:
            for s in generate_from_tree(c, max_repetitions):
                if s not in seen:
                    seen.add(s)
                    yield s

    elif node.kind == 'concat':
        partial = [""]
        for c in node.children:
            new_partial = []
            child_strings = list(generate_from_tree(c, max_repetitions))
            for p in partial:
                for s in child_strings:
                    new_partial.append(p + s)
            partial = new_partial

        seen = set(partial)
        for val in seen:
            yield val


def generate_cre_final(regex, max_repetitions=3):
    tree = parse_regex(regex)
    for word in generate_from_tree(tree, max_repetitions):
        yield word if word != "" else "ɛ"

if __name__ == "__main__":
    test_cases = []
    for line in open("TestSuiteFiles/TestSuite1_CREs.txt"):
        test_cases.append(line.rstrip())

    output_file = open("TestSuiteFiles/TestSuite1_Inputs.txt", 'w')
    for pattern in test_cases:
        results = sorted(generate_cre_final(pattern, 3))
        for word in results: 
            output_file.write(word + ", ")
        output_file.write("\n")