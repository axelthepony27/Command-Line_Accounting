from text_parser import FileParser
from data import Transaction, Posting
from treelib import Tree


class Reporter:
    def __init__(self, filename: str):
        self.parser = FileParser(filename)
        self.parser.parse()
        self.accounts = Tree()
        self.accounts.create_node(tag="root", identifier="root")
        self.build_accounts()

    def build_accounts(self):
        for txn in self.parser.transactions:
            for posting in txn.postings:
                account_names = posting.account.split(":")
                for i in range(len(account_names)):
                    account = account_names[i]
                    parent = None
                    if i > 0:
                        parent = account_names[i - 1]
                    self.add_account(account, parent)

    def add_account(self, account: str, parent: str = None):
        #print(self.accounts)
        if self.accounts.contains(account.lower()):
            return
        if parent is None:
            self.accounts.create_node(tag=account, identifier=account.lower(), parent="root")
            return
        if self.accounts.contains(parent.lower()):
            self.accounts.create_node(tag=account, identifier=account.lower(), parent=parent.lower())
            return

    def balance_txn(self, txn: Transaction):
        posting: Posting
        total = 0
        for posting in txn.postings:
            total += posting.amount.quantity

    def balance(self, filename: str):
        parser = FileParser(filename)
        parser.parse()
        report = []
        txn: Transaction
        for txn in parser.transactions:
            print(txn.description())


reporter = Reporter("../ledger-sample-files/Income.ledger")
print(reporter.accounts)
