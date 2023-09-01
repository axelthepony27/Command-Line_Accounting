from text_parser import FileParser
from data import Transaction, Amount, Posting
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
        if self.accounts.contains(account.lower()):
            return
        if parent is None:
            self.accounts.create_node(tag=account, identifier=account.lower(), parent="root")
            return
        if self.accounts.contains(parent.lower()):
            self.accounts.create_node(tag=account, identifier=account.lower(), parent=parent.lower())
            return

    @staticmethod
    def balance_txn_per_commodity(txn: Transaction, commodity: str):
        total = 0
        elided = []
        postings = txn.filter_per_commodity(commodity)
        for posting in postings:
            if posting.amount is None:
                elided.append(posting)
            else:
                total += posting.amount.quantity
        if not elided:
            return total == 0
        else:
            difference = -total / len(elided)
            for elided_posting in elided:
                elided_posting.amount = Amount(quantity=f"{difference}", commodity=commodity, is_currency=postings[1]
                                               .amount.is_currency)
            return True

    def balance_txn(self, txn: Transaction):
        #balanced = True
        #print(txn.get_commodities())
        #for commodity in txn.get_commodities():
        #    balanced = balanced and self.balance_txn_per_commodity(txn, commodity)

        total = 0
        elided = []
        #postings = txn.filter_per_commodity(commodity)
        postings = txn.postings
        for posting in postings:
            if posting.amount is None:
                elided.append(posting)
            else:
                total += posting.amount.quantity
        if not elided:
            return total == 0
        else:
            difference = -total / len(elided)
            for elided_posting in elided:
                elided_posting.amount = Amount(quantity=f"{difference}", commodity=postings[0].amount.commodity,
                                               is_currency=postings[0].amount.is_currency)
            return True

    def balance(self):
        report = []
        txn: Transaction
        for txn in self.parser.transactions:
            print(txn.description())
            print("Balanced: " + str(self.balance_txn(txn)))
            print("--------------------------")


reporter = Reporter("../ledger-sample-files/Bitcoin.ledger")
reporter.balance()
