# Introduction
A very simple IPFS CID scraper for [Foundation.app](https://foundation.app/).

**Disclaimer**: I am not a coding coder, I wrote this in a day to save me from manually creating the resulting json file and I thought maybe someone else might find this useful. This script has basically no checks in it so please feed it valid URLs and is liable to break if Foundation change their page structure, it has no rate limits either so if you have a Robek sized collection maybe split your batches up, idk how Foundation will feel about 500+ requests at once...

# Flags
```bash
# default flags
-h, --help          shows the help message
-v, --version       shows the version number

# url related flags, url or batch is required
-u, --url           pass a single url
-b, --batch         pass a file of urls, one per line

# file related flags
-i, --input         specify an existing json file to append (optional)
```

# Result Structure
This script creates a simple json structure that aims to be easy to import into IPFS while also remaining human readable for manual editing should the need arise, an example output from two artworks is below:

```json
[
    {
        "name": "Aquatic Alchemy",
        "metadata": "QmW6hT4ZN5jmsfCrMwzCSiym5wVEyYExMfvvVwQVJw9K3x",
        "media": "QmP5aVp9E7u2tYz39HTfM4spHgyBxXVCNJ2EGrZMqdJKWB"
    },
    {
        "name": "Over the rainbow",
        "metadata": "QmQM4PDUTMkahF5nhZEuE1HNZjmvQTJsX5Cnz46AURT2KD",
        "media": "QmXbj7KkpDVvcxyCA9KNNgryrG1NpTgiFW3At1dPR85NiD"
    }
]
```

# Pinning with IPFS
To pin the resulting CIDs with IPFS use [jq](https://github.com/stedolan/jq) on the command-line to pipe the CID value into IPFS. A few examples are below:

* All CIDs to a local IPFS node
```bash
jq -r 'del(.[]| .name) | .[].[]' results.json | ipfs pin add
```
```bash
QmW6hT4ZN5jmsfCrMwzCSiym5wVEyYExMfvvVwQVJw9K3x
QmP5aVp9E7u2tYz39HTfM4spHgyBxXVCNJ2EGrZMqdJKWB
QmQM4PDUTMkahF5nhZEuE1HNZjmvQTJsX5Cnz46AURT2KD
QmXbj7KkpDVvcxyCA9KNNgryrG1NpTgiFW3At1dPR85NiD
```
* Selecting a specific artwork

```bash
jq -r '.[] | select(.name=="Aquatic Alchemy") | .metadata, .media' results.json
```
```bash
QmW6hT4ZN5jmsfCrMwzCSiym5wVEyYExMfvvVwQVJw9K3x
QmP5aVp9E7u2tYz39HTfM4spHgyBxXVCNJ2EGrZMqdJKWB
```
* Metadata only to a remote IPFS node

```bash
jq -r '.[].metadata' results.json | ipfs --api /ip4/69.69.69.69/tcp/5001 pin add
```
```bash
QmW6hT4ZN5jmsfCrMwzCSiym5wVEyYExMfvvVwQVJw9K3x
QmQM4PDUTMkahF5nhZEuE1HNZjmvQTJsX5Cnz46AURT2KD
```
