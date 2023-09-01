from datetime import datetime

from scripts.text_parser import FileParser
from scripts.data import Transaction, Amount
from treelib import Tree, Node


def build_accounts(transactions: list[Transaction]):
    accounts = Tree()
    accounts.create_node(tag="root", identifier="root")
    for txn in transactions:
        for posting in txn.postings:
            account_names = posting.account.split(":")
            for i in range(len(account_names)):
                account = account_names[i]
                parent = None
                if i > 0:
                    parent = account_names[i - 1]
                if posting.amount is None:
                    add_account(account=account, accounts=accounts, data=Amount.parse("$0"), parent=parent)
                else:
                    add_account(account=account, accounts=accounts, data=posting.amount, parent=parent, )
    return accounts


def add_account(account: str, accounts: Tree, data: Amount = None, parent: str = None):
    if accounts.contains(account.lower()):
        if data is None:
            return
        else:
            # print(accounts.get_node(account.lower()))
            accounts.get_node(account.lower()).data.quantity = (
                    accounts.get_node(account.lower()).data.quantity + data.quantity)
            return
    if parent is None:
        accounts.create_node(tag=account, identifier=account.lower(), parent="root", data=data)
        return
    if accounts.contains(parent.lower()):
        accounts.create_node(tag=account, identifier=account.lower(), parent=parent.lower(), data=data)
        return


def balance_txn_per_commodity(txn: Transaction, commodity: str):
    total = 0
    elided = []
    postings = txn.filter_by_commodity(commodity)
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


def balance(transactions: list[Transaction]):
    for txn in transactions:
        if not balance_txn(txn):
            print("The following transaction is not balanced!")
            print(txn.description())
            return False
    return True


def filter_node(node: Node, account_names: list[str] = None):
    if account_names.__contains__(node.identifier):
        return True


def balance_report(parser: FileParser, account_names: list[str] = None):
    transactions = parser.transactions
    accounts = build_accounts(transactions)
    elements = []
    if account_names:
        temp = Tree()
        temp.create_node(tag="root", identifier="root")
        for account_name in account_names:
            account_name = account_name.lower()
            if accounts.contains(account_name) and not temp.contains(account_name):
                temp.paste("root", accounts.subtree(account_name))
        if temp.size() > 1:
            accounts = temp
    if balance(transactions):
        total = Amount.parse("$0")
        for account in accounts.all_nodes():
            if account.data is None:
                account.data = Amount.parse("$0")
            if account.tag != "root":
                elements.append([account.data.format(), account.tag])
                if account.is_leaf():
                    total.quantity += account.data.quantity
        elements.append(["---------------", ""])
        elements.append([total.format(), ""])
        return elements
    else:
        print("------- FAILED TO PRINT REPORT -------")


def register_report(parser: FileParser, account_names: list[str] = None):
    transactions = parser.transactions
    elements = []
    if balance(transactions):
        running_total = Amount.parse("$0")
        for txn in transactions:
            postings = txn.filter_by_accounts(account_names)
            if postings:
                running_total.quantity += postings[0].amount.quantity
                new_date = datetime.strptime(str(txn.date), '%Y-%m-%d').strftime('%d-%b-%Y')
                elements.append([new_date, txn.payee, postings[0].account, postings[0].amount.format(),
                                 running_total.format()])
                for posting in postings[1:]:
                    running_total.quantity += posting.amount.quantity
                    elements.append(["", "", posting.account, posting.amount.format(), running_total.format()])
        return elements
    else:
        print("------- FAILED TO PRINT REPORT -------")


def print_report(parser: FileParser):
    for txn in parser.transactions:
        print(txn.description())


def report(parser: FileParser, report_type: str, account_names: list[str] = None):
    match report_type:
        case "BALANCE":
            return balance_report(parser, account_names)
        case "REGISTER":
            return register_report(parser, account_names)
        case "PRINT":
            print_report(parser)
