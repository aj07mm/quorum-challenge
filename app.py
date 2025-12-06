import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


legislators = read_csv('legislators.csv')
bills = read_csv('bills.csv')
votes = read_csv('votes.csv')
vote_results = read_csv('vote_results.csv')

"""
1. For every legislator in the dataset,
    how many bills did the legislator support (voted for the bill)?
    How many bills did the legislator oppose?

2. For every bill in the dataset,
    how many legislators supported the bill?
    How many legislators opposed the bill?
    Who was the primary sponsor of the bill?
"""

def process_legislator_dataset(legislators, votes, vote_results):
    legislators_bills = {}
    for legislator in legislators:
        legislator_id = legislator['id']
        legislator_name = legislator['name']
        supported_count = 0
        opposed_count = 0

        if legislator_id not in legislators_bills:
            legislators_bills[legislator_id] = {
                    'name': legislator_name, 'supported_bills': [], 'opposed_bills': []}

        for vote_result in vote_results:
            if vote_result['legislator_id'] == legislator_id:
                vote = next((v for v in votes  if v['id'] == vote_result['vote_id']), None)
                if vote_result['vote_type'] == '1': # yes
                    legislators_bills[legislator_id]['supported_bills'].append(vote['bill_id'])
                if vote_result['vote_type'] == '2': # no
                    legislators_bills[legislator_id]['opposed_bills'].append(vote['bill_id'])

    return legislators_bills

def process_bill_dataset():
    pass


legislators = process_legislator_dataset(legislators, votes, vote_results)
for k, v in legislators.items():
    print(k, v['name'], len(set(v['supported_bills'])), len(set(v['opposed_bills'])))
