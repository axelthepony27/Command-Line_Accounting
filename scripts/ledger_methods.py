import decimal

from text_parser import FileParser
from data import Transaction, Amount, Posting
from treelib import Tree
from decimal import Decimal


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
                    if posting.amount is None:
                        self.add_account(account=account, parent=parent)
                    else:
                        self.add_account(account=account, data=posting.amount, parent=parent)

    def add_account(self, account: str, data: Amount = None, parent: str = None):
        if self.accounts.contains(account.lower()):
            if data is None:
                return
            else:
                self.accounts.get_node(account.lower()).data.quantity = (
                        self.accounts.get_node(account.lower()).data.quantity + data.quantity)
                return
        if parent is None:
            self.accounts.create_node(tag=account, identifier=account.lower(), parent="root", data=data)
            return
        if self.accounts.contains(parent.lower()):
            self.accounts.create_node(tag=account, identifier=account.lower(), parent=parent.lower(), data=data)
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

    @staticmethod
    def balance_txn(txn: Transaction):
        # balanced = True
        # print(txn.get_commodities())
        # for commodity in txn.get_commodities():
        #    balanced = balanced and self.balance_txn_per_commodity(txn, commodity)

        total = 0
        elided = []
        # postings = txn.filter_per_commodity(commodity)
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
        txn: Transaction
        for txn in self.parser.transactions:
            if not self.balance_txn(txn):
                print("The following transaction is not balanced!")
                print(txn.description())
                return False
        return True

    def report(self, report_type: str):
        match report_type:
            case "BALANCE":
                if self.balance():
                    total = Amount.parse("$0")
                    for account in self.accounts.all_nodes():
                        if account.data is None:
                            account.data = Amount.parse("$0")
                        if account.tag != "root":
                            print(account.data.format() + " " + account.tag)
                            if account.is_leaf():
                                total.quantity += account.data.quantity
                    print("----------")
                    print(total.format())
                else:
                    print("------- FAILED TO PRINT REPORT -------")


reporter = Reporter("../ledger-sample-files/Income.ledger")
reporter.report("BALANCE")
