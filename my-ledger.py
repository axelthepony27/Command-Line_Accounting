#!/usr/bin/env python3

from pathlib import Path

import typer
from typing import Optional, List
from typing_extensions import Annotated

from rich import print
from rich.console import Console
from rich.table import Table

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
        elements = report(parser, "BALANCE", accounts)
        table = Table(box=None)
        for element in elements:
            table.add_row(element[0], f"[blue]{element[1]}[/blue]")
        table.columns[0].justify = "right"
        console = Console()
        console.print(table)
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
        elements = report(parser, "REGISTER", accounts)
        table = Table(box=None)
        for element in elements:
            table.add_row(f"[green]{element[0]}[/green]", element[1], f"[blue]{element[2]}[/blue]", element[3], element[4])
        table.columns[3].justify = "right"
        table.columns[4].justify = "right"
        console = Console()
        console.print(table)
    elif not file.exists():
        print("The requested file doesn't exist")


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
