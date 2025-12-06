import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


legislators = read_csv('legislators.csv')
bills = read_csv('bills.csv')
votes = read_csv('votes.csv')
vote_results = read_csv('vote_results.csv')
