
def normalize(s):
    parentheses = s[s.find('('):s.find(')') + 1]
    s = s.replace(parentheses, '')

    sq_brackets = s[s.find('['):s.find(']') + 1]
    s = s.replace(sq_brackets, '')

    s = s.lstrip()
    s = s.rstrip()
    return s
