import datetime


class Posting:

    def __init__(self, account: str, amount: float, commodity: str):
        self.account = account
        self.amount = amount
        self.commodity = commodity

    def description(self):
        return f"{self.account}    {self.commodity}{self.amount}"


class Transaction:

    def __init__(self, date: datetime.date, payee: str, postings: list[Posting]):
        self.date = date
        self.payee = payee
        self.postings = postings

    def description(self):
        x = ""
        for posting in self.postings:
            x += posting.description() + "\n"
        return f"{self.date}    {self.payee}, \n{x}"


posting1 = Posting("Expenses:Food", 20, "$")
posting2 = Posting("Assets:Checking", -20, "$")
txn = Transaction(datetime.date.today(), "Awesome Food Payee", [posting1, posting2])
print(txn.description())
