#!/usr/bin/env python3

import typer
from typing_extensions import Annotated

from scripts.text_parser import FileParser
from scripts.ledger_methods import report


app = typer.Typer()


@app.command()
def hello(name: str):
    """Takes in a string, returns a salutation."""
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def balance(filename: Annotated[str, typer.Argument()] = "./ledger-sample-files/index.ledger"):
    """Parses the given file."""
    parser = FileParser(filename)
    parser.parse()
    report(parser, "BALANCE")


@app.command()
def register(filename: str):
    """Parses the given file."""
    parser = FileParser(filename)
    parser.parse()


@app.command()
def print(filename: str):
    """Parses the given file."""
    parser = FileParser(filename)
    parser.parse()


if __name__ == "__main__":
    app()
