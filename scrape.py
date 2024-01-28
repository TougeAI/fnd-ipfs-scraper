import requests, json, os, argparse
from bs4 import BeautifulSoup
from datetime import datetime

# cli args
parser = argparse.ArgumentParser(prog='Foundation IPFS Scraper' ,description="Extracts IPFS CIDs from artwork on Foundation.app", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.1')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-b", "--batch", help="batch input file, one url per line")
group.add_argument("-u", "--url", help="single url")
parser.add_argument("-i", "--input", default='', help="specify an existing json file to append")
args = parser.parse_args()

# file
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
filepath = (args.input)

try:
    with open(filepath) as i:
        data = json.load(i)
except FileNotFoundError:
    data = []

# url or batch input
if args.url is not None:
    urls = [args.url]
else:
    with open(args.batch) as b:
        urls = b.read().splitlines()

# json builder
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    result = json.loads(soup.find(id="__NEXT_DATA__").get_text())
    if (result['props']['pageProps']['artwork']['assetIPFSPath']) is not None:
        name = (result['props']['pageProps']['artwork']['name'])
        media = os.path.split(os.path.split((result['props']['pageProps']['artwork']['assetIPFSPath']))[0])[1]
        metadata = os.path.split(os.path.split((result['props']['pageProps']['artwork']['metadataIPFSPath']))[0])[1]
        entry = {'name': name, 'metadata': metadata, 'media': media}
        data.append(entry)

# output
try:
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
except FileNotFoundError:
    with open(timestamp+'-fnd.json', 'w') as f:
        json.dump(data, f, indent=4)