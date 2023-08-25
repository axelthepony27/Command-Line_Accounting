import re


def read(filename):
    with open(filename) as f:
        return f.readlines()


def choose_parsing_state(line):
    if re.search('^[0-9]', line):
        return "TRANSACTION"
    elif re.search('^;', line):
        return "COMMENT"
    elif re.search('^P', line):
        return "COMMODITY"
    else:
        return "DEFAULT"


def parsing_state(state):
    match state:
        case "TRANSACTION":
            return "We are now inside a transaction"
        case "COMMENT":
            return "We are now inside a comment"
        case "COMMODITY":
            return "We are now inside a commodity"


def parse(filename):
    lines = read(filename)
    for line in lines:
        print(parsing_state(choose_parsing_state(line)))


parse("../ledger-sample-files/Income.ledger")
