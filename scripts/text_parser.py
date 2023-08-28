import re
import datetime
from scripts.data import Transaction, Posting, Amount


class FileParser:
    def __init__(self, filename: str):
        self.lines = FileParser.read(filename)
        self.index = 0
        self.current_line = self.lines[self.index]
        self.state = "DEFAULT"

    @staticmethod
    def read(filename):
        with open(filename) as f:
            return f.readlines()

    def next_line(self):
        self.index += 1
        if self.index == len(self.lines):
            self.current_line = None
        else:
            self.current_line = self.lines[self.index]

    def choose_parsing_state(self):
        if re.search('^[0-9]', self.current_line):
            self.state = "TRANSACTION"
        elif re.search('^;', self.current_line):
            self.state = "COMMENT"
        elif re.search('^P', self.current_line):
            self.state = "COMMODITY"
        else:
            self.state = "DEFAULT"

    def parse_line(self):
        self.choose_parsing_state()
        match self.state:
            case "TRANSACTION":
                txn = self.parse_transaction()
                print(txn.description())
            case "COMMENT":
                print("We are now inside a comment")
            case "COMMODITY":
                print("We are now inside a commodity")
            case "DEFAULT":
                print(self.current_line)

    def parse_transaction(self):
        split_line = self.current_line.split(" ", 1)
        date_list = split_line[0].split("/")
        date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        txn = Transaction(date, split_line[1])

        postings = []
        flag = True
        while flag:
            if self.index+1 < len(self.lines):
                next_line = self.lines[self.index+1]
                if re.search('^\s', next_line):
                    self.next_line()
                    postings.append(self.parse_posting())
                    continue
                else:
                    flag = False
                    continue
            else:
                flag = False
                continue

        txn.postings = postings
        return txn

    def parse_posting(self):
        posting_elements = re.split(r'\s{2,}', self.current_line)
        if len(posting_elements) == 1:
            return Posting(posting_elements[0])
        else:
            return Posting(posting_elements[0], Amount.parse(posting_elements[1]))

    def parse(self):
        while self.index < len(self.lines):
            self.parse_line()
            self.next_line()
