#!/usr/bin/python

import datetime
import csv

input_file = 'Transactions.csv'
output_file = 'input.csv'
output_file_stats = 'stats.csv'
separator = ','
ignore_first_line = True

transactions = {}
transactions_stats = {}
counters = {}

def file_lengthy(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def my_split(line, sep):
    cells = []
    word = ''
    has_comma = False
    for c in line:
        if c != sep:
            if c != '"':
                word += c
            else:
                if not has_comma:
                    has_comma = True
                else:
                    has_comma = False
        else:
            if has_comma:
                word += c
            else:
                cells.append(word)
                word = ''
                has_comma = False
    return cells

# read each line, store transactions
def read_line(line):
    cells = my_split(line, separator)
    
    in_date = datetime.datetime.strptime(cells[0], '%d-%m-%Y').strftime('%Y-%m-%d')
    in_company = cells[2] # symbol title
    in_key = cells[3] # that's the stock's key/id
    in_amount = int(cells[5]) # nr. shares
    in_price = float(cells[7].replace(',', '.').replace('"', '')) # price per share

    if not in_key in counters:
        counters[in_key] = {'id': -1, 'amount': 0}
    
    counters[in_key]['id'] = counters[in_key]['id'] + 1
    counters[in_key]['amount'] = counters[in_key]['amount'] + in_amount

    out_id = counters[in_key]['id']
    out_type = 'Buy' if in_amount > 0 else 'Sell'
    out_amount = in_amount if in_amount >= 0 else in_amount * -1
    out_amount_accumulated = counters[in_key]['amount']
    loss_valid = 'true' if out_type == 'Sell' else ''

    # csv
    if not in_key in transactions:
        transactions[in_key] = []
    transactions[in_key].append([in_key, out_id, out_type, in_date, out_amount, in_price, loss_valid])

    # stats
    if not in_key in transactions_stats:
        transactions_stats[in_key] = {'date': in_date, 'title': in_company, 'buy_amount': 0, 'sell_amount': 0, 'buy_value': 0, 'sell_value': 0}
    amount_key = 'buy_amount' if out_type == 'Buy' else 'sell_amount'
    value_key = 'buy_value' if out_type == 'Buy' else 'sell_value'
    transactions_stats[in_key][amount_key] = transactions_stats[in_key][amount_key] + in_amount
    transactions_stats[in_key][value_key] = round(transactions_stats[in_key][value_key] + out_amount * in_price, 2)

def write_transactions(csv_writer):
    for key, trans in transactions.items():
        for row in trans:
            csv_writer.writerow(row)

def write_transactions_stats(csv_writer):
    headers = ['Datum', 'Naziv', 'Nakup (kos)', 'Prodaja (kos)', 'Nakupna vrednost', 'Prodajna vrednost', 'Realizacija']
    csv_writer.writerow(headers)
    for key, trans in transactions_stats.items():
        buy_value = trans['buy_value']
        sell_value = trans['sell_value']
        gain_pct = round((sell_value - buy_value) / buy_value * 100, 2)
        csv_writer.writerow([trans['date'], trans['title'], trans['buy_amount'], trans['sell_amount'], trans['buy_value'], trans['sell_value'], gain_pct])

# read inpupt data in reversed order
file = open(input_file, 'r')
file_reversed = reversed(list(file))

ln = file_lengthy(input_file)
for line in file_reversed:
    ln = ln - 1
    if not (ignore_first_line and ln == 0):
        read_line(line)

file.close()

with open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    write_transactions(csv_writer)
with open(output_file_stats, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    write_transactions_stats(csv_writer)
