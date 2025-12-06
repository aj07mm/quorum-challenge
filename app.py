import csv


INPUT_FILES_PATH = './input_files/'
OUTPUT_FILES_PATH = './input_files/'


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(filename, fieldnames, rows):
    """Write data to a CSV file."""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


legislators = read_csv(INPUT_FILES_PATH + 'legislators.csv')
bills = read_csv(INPUT_FILES_PATH + 'bills.csv')
votes = read_csv(INPUT_FILES_PATH + 'votes.csv')
vote_results = read_csv(INPUT_FILES_PATH + 'vote_results.csv')


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


write_csv(
    filename=OUTPUT_FILES_PATH + 'legislator_stats.csv',
    fieldnames=['legislator_id', 'name', 'supported_bills', 'opposed_bills'],
    rows=[{
        'legislator_id': k,
        'name': v['name'],
        'supported_bills': len(set(v['supported_bills'])),
        'opposed_bills': len(set(v['opposed_bills']))
    } for k, v in process_legislator_dataset(legislators, votes, vote_results).items()]
)
write_csv(
    filename=OUTPUT_FILES_PATH + 'bills_stats.csv',
    fieldnames=['bill_id', 'primary_sponsor', 'supported_legislators', 'opposed_legislators'],
    rows=[{
        'bill_id': k,
        'primary_sponsor': v['primary_sponsor'],
        'supported_legislators': len(set(v['supported_legislators'])),
        'opposed_legislators': len(set(v['opposed_legislators']))
    } for k, v in process_bill_dataset(bills, votes, vote_results).items()]
)
