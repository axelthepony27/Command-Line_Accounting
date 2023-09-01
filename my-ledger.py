#!/usr/bin/env python3
from pathlib import Path
from typing import Optional, List

import typer
from typing_extensions import Annotated

from scripts.text_parser import FileParser
from scripts.ledger_methods import report

app = typer.Typer()


@app.command()
def balance(file: Annotated[Path, typer.Option()] = "./ledger-sample-files/index.ledger",
            accounts: Annotated[Optional[List[str]], typer.Argument()] = None):
    """Find the balance of the selected file and accounts.
    Leave arguments blank to find the balances of all of your accounts."""
    if file is None:
        print("No file")
        raise typer.Abort()
    if file.is_file():
        parser = FileParser(str(file))
        parser.parse()
        report(parser, "BALANCE", accounts)
    elif not file.exists():
        print("The requested file doesn't exist exist")


@app.command()
def register(file: Annotated[Path, typer.Option()] = "./ledger-sample-files/index.ledger",
             accounts: Annotated[Optional[List[str]], typer.Argument()] = None):
    """Shows all transactions of selected file and accounts, and a running total.
    Leave arguments blank to find to show all of your transactions."""
    if file is None:
        print("No file")
        raise typer.Abort()
    if file.is_file():
        parser = FileParser(str(file))
        parser.parse()
        report(parser, "REGISTER", accounts)
    elif not file.exists():
        print("The requested file doesn't exist exist")


@app.command("print")
def print_report(file: Annotated[Path, typer.Option()] = "./ledger-sample-files/index.ledger"):
    """Prints out ledger transactions in a textual format that can be parsed by Ledger."""
    if file is None:
        print("No file")
        raise typer.Abort()
    if file.is_file():
        parser = FileParser(str(file))
        parser.parse()
        report(parser, "PRINT")
    elif not file.exists():
        print("The requested file doesn't exist exist")


if __name__ == "__main__":
    app()
