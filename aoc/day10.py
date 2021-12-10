from . import util


MATCHING = {
    "(" : ")",
    "[" : "]",
    "{" : "}",
    "<" : ">",
}


SYNTAX_ERROR_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


AUTOCOMPLETE_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def get_lines(lines):
    return [line for line in lines if line]


def find_first_illegal_character(line):
    stack = []
    expected = None

    for i, c in enumerate(line):
        if c in MATCHING:
            # Opening brackets are always legal.
            stack.append(c)
            expected = MATCHING[c]
        elif c == expected:
            # Chunk closed by correct closing bracket.
            stack.pop()
            expected = MATCHING[stack[-1]] if stack else None
        else:
            # Line is corrupted, return the offending character.
            return c, None

    # Line is incomplete rather than corrupted, return the stack of unmatched
    # characters for use by autocompletion.
    return None, stack


def calculate_autocomplete_score(unmatched):
    # The sequence of closing characters is found by matching each unmatched
    # opening bracket in reverse order, closing the most recent chunk first.
    score = 0
    for c in reversed(unmatched):
        score *= 5
        score += AUTOCOMPLETE_SCORE[MATCHING[c]]
    return score


def run():
    inputlines = util.get_input_lines("10.txt")
    lines = get_lines(inputlines)

    total_syntax_error_score = 0
    autocomplete_scores = []

    for line in lines:
        illegal, unmatched = find_first_illegal_character(line)
        if illegal:
            score = SYNTAX_ERROR_SCORE[illegal]
            total_syntax_error_score += score
        else:
            score = calculate_autocomplete_score(unmatched)
            autocomplete_scores.append(score)

    middle_autocomplete_score = \
        sorted(autocomplete_scores)[len(autocomplete_scores) // 2]

    return total_syntax_error_score, middle_autocomplete_score
