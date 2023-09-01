import datetime
import decimal
import re


class Amount:
    currency_dict = {
        "USD": "$",
        "GBP": "£"
    }

    def __init__(self, quantity: decimal.Decimal | str | int, commodity: str, is_currency: bool = False):
        self.quantity = decimal.Decimal(quantity)
        self.commodity = commodity
        self.is_currency = is_currency

    def description(self):
        return f"{self.quantity}    {self.commodity}"

    @staticmethod
    def get_symbol_from_name(name: str):
        return Amount.currency_dict.get(name)

    @staticmethod
    def get_name_from_symbol(symbol: str):
        for key, value in Amount.currency_dict.items():
            if symbol == value:
                return key

        return "key doesn't exist"

    @staticmethod
    def parse(string: str):
        pattern = r"[^a-zA-Z0-9\s.,\/@-]"
        elements = string.split()
        if len(elements) == 2:
            return Amount(decimal.Decimal(elements[0]), elements[1])
        else:
            elements = re.split(pattern, string)
            symbol = re.search(pattern, string)
            commodity = Amount.get_name_from_symbol(symbol.group(0))
            if elements[0] == '-':
                quantity = decimal.Decimal(elements[1])
                return Amount(-quantity, commodity, True)
            else:
                quantity = decimal.Decimal(elements[1])
                return Amount(quantity, commodity, True)

    def format(self):
        if not self.is_currency:
            return f"{self.quantity} {self.commodity}"
        else:
            if self.quantity >= 0:
                return "{symbol}{quantity:,.2f}".format(symbol=Amount.get_symbol_from_name(self.commodity),
                                                        quantity=self.quantity)
            else:
                return "-{symbol}{quantity:,.2f}".format(symbol=Amount.get_symbol_from_name(self.commodity),
                                                         quantity=self.quantity.__abs__())


class Posting:
    def __init__(self, account: str, amount: Amount = None):
        self.account = account
        self.amount = amount

    def description(self):
        if self.amount is None:
            return f"{self.account}"
        else:
            return f"{self.account}    {self.amount.format()}"

    def to_string(self):
        if self.amount is None:
            print("Account:: " + str(self.account) + "       Amount:: Elided")
        else:
            print("Account:: " + str(self.account) + "       Amount:: " + self.amount.format())


class Transaction:

    def __init__(self, date: datetime.date, payee: str, postings: list[Posting] = None):
        self.date = date
        self.payee = payee
        self.postings = postings

    def description(self):
        x = ""
        if self.postings is not None:
            for posting in self.postings:
                x += posting.description() + "\n"
            return f"{self.date}    {self.payee} \n{x}"
        else:
            return f"{self.date}    {self.payee} No postings"

    def get_commodities(self):
        commodities = []
        for posting in self.postings:
            if posting.amount is not None and not (commodities.__contains__(posting.amount.commodity)):
                commodities.append(posting.amount.commodity)
        return commodities

    def filter_per_commodity(self, commodity: str):
        filtered_postings = []
        for posting in self.postings:
            if posting.amount is not None and posting.amount.commodity == commodity:
                filtered_postings.append(posting)
        return filtered_postings

    def to_string(self):
        print(f"Date: {self.date}")
        print(f"Payee: {self.payee}")
        print("Postings:")
        for posting in self.postings:
            posting.to_string()


posting1 = Posting("Expenses:Food", Amount(20, 'USD', True))
posting2 = Posting("Assets:Checking", Amount(-20, "GBP", True))
txn = Transaction(datetime.date.today(), "Awesome Food Payee", [posting1, posting2])
txn2 = Transaction(datetime.date.today(), "Another awesome payee")

# print(txn.description())
# print()
# print(Amount.get_symbol_from_name("USD"))
# print(Amount.get_name_from_symbol("$"))
# print(Amount.parse("-20 BTC").description())
# print("-----")
# amount = Amount.parse("$20")
# print(amount.description())
# amount2 = Amount.parse("-$20")
# print(amount2.description())
# print("-----")
# amount3 = Amount(-20, "USD", True)
# print(amount3.format())
