# Command-Line_Accounting
## To run the program
First, make sure to make the `my-ledger.py` file executable. In you Command Line, run
```
$ chmod +x my-ledger.py
```
With that, you now can directly run our script with `./my-ledger.py`.
## Available commands
The app counts with a total of 3 available commands: `balance`, `register` and `print`.

### `balance`
Run
```
./my-ledger.py balance [--file PATH-TO-FILE] [--sorted date | payee] [ACCOUNT1 ACCOUNT2...]
```
to find the balance of the selected file and accounts. Leave arguments blank to find the balances of all of your accounts, sorted by date.

### `reegister`
Run
```
./my-ledger.py register [--file PATH-TO-FILE] [--sorted date | payee] [ACCOUNT1 ACCOUNT2...]
```
to show all transactions of selected file and accounts, and a running total. Leave arguments blank to show all of your transactions, sorted by date.

### `print`
Run
```
./my-ledger.py print [--file PATH-TO-FILE] [--sorted date | payee]
```
to print out ledger transactions in a textual format that can be parsed by Ledger. Leave arguments blank to show all of your transactions, sorted by date.
