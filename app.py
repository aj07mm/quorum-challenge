import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


legislators = read_csv('legislators.csv')
bills = read_csv('bills.csv')
votes = read_csv('votes.csv')
vote_results = read_csv('vote_results.csv')


def process_legislator_dataset(legislators, votes, vote_results):
    """
    1. For every legislator in the dataset,
        how many bills did the legislator support (voted for the bill)?
        How many bills did the legislator oppose?
    """
    acc = {}
    for legislator in legislators:
        legislator_id = legislator['id']
        legislator_name = legislator['name']

        if legislator_id not in acc:
            acc[legislator_id] = {
                    'name': legislator_name, 'supported_bills': [], 'opposed_bills': []}

        for vote_result in vote_results:
            if vote_result['legislator_id'] == legislator_id:
                vote = next((v for v in votes  if v['id'] == vote_result['vote_id']), None)
                if vote_result['vote_type'] == '1': # yes
                    acc[legislator_id]['supported_bills'].append(vote['bill_id'])
                if vote_result['vote_type'] == '2': # no
                    acc[legislator_id]['opposed_bills'].append(vote['bill_id'])

    return acc

def process_bill_dataset(bills, votes, vote_results):
    """"
    2. For every bill in the dataset,
        how many legislators supported the bill?
        How many legislators opposed the bill?
        Who was the primary sponsor of the bill?
    """
    acc = {}
    for bill in bills:
        bill_id = bill['id']
        bill_title = bill['title']
        primary_sponsor = bill['sponsor_id']

        if bill_id not in acc:
            acc[bill_id] = {
                'primary_sponsor': primary_sponsor,
                'supported_legislators': [],
                'opposed_legislators': []
            }

        for vote_result in vote_results:
            for vote in votes:
                if vote_result['vote_id'] == vote['id']:
                    if vote['bill_id'] == bill_id:
                        if vote_result['vote_type'] == '1': # yes
                            acc[bill_id]['supported_legislators'].append(vote_result['legislator_id'])
                        if vote_result['vote_type'] == '2': # no
                            acc[bill_id]['opposed_legislators'].append(vote_result['legislator_id'])

    return acc


legislators = process_legislator_dataset(legislators, votes, vote_results)
for k, v in legislators.items():
    print(k, v['name'], len(set(v['supported_bills'])), len(set(v['opposed_bills'])))

bills = process_bill_dataset(bills, votes, vote_results)
for k, v in bills.items():
    print(k, v['primary_sponsor'], len(set(v['supported_legislators'])),
          len(set(v['opposed_legislators'])))



