#!/usr/bin/env python3

import typer
from typing_extensions import Annotated

from scripts.text_parser import FileParser
from scripts.ledger_methods import report


app = typer.Typer()


@app.command()
def balance(filename: Annotated[str, typer.Argument()] = "./ledger-sample-files/index.ledger"):
    """Find the balance of the selected file and accounts.
    Leave arguments blank to find the balances of all of your accounts."""
    parser = FileParser(filename)
    parser.parse()
    report(parser, "BALANCE")


@app.command()
def register(filename: Annotated[str, typer.Argument()] = "./ledger-sample-files/index.ledger"):
    """Shows all transactions of selected file and accounts, and a running total.
    Leave arguments blank to find to show all of your transactions."""
    parser = FileParser(filename)
    parser.parse()
    report(parser, "REGISTER")


@app.command()
def print(filename: Annotated[str, typer.Argument()] = "./ledger-sample-files/index.ledger"):
    """Prints out ledger transactions in a textual format that can be parsed by Ledger."""
    parser = FileParser(filename)
    parser.parse()
    report(parser, "PRINT")


if __name__ == "__main__":
    app()
