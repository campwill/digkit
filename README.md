# digkit (Digital Forensics Toolkit)

A command-line Python tool for looking up application and device information, collecting and parsing data from various sources, and generating file hashes.

## Installation

```bash
git clone https://github.com/campwill/digkit.git
cd digkit
pip install .
```

This installs `digkit` as a command-line tool.

## Usage

```bash
digkit [-h] <command> ...
```

## Commands

#### `lookup`

Look up information associated with application and device identifiers.

* **bundleid**: Look up information associated with a domain name.

* **domain**: Identifies application names from bundle IDs across app stores (Apple, Google, and Galaxy).
  * **whois**: Search for WHOIS information associated with a domain name.
  * **dns**: Search for DNS record associated with a domain name.

* **iccid**: Decodes information from an Integrated Circuit Card Identifier (ICCID) number.

#### `parse`

Collect, process, and parse information from various data sources.

* **database**: Parses notable artifacts from a selection of supported databases:
  * `dwbcommon`: Decodes usage events from dwbCommon.db.
  * `notestore`: Extracts Apple secure note hashes (in hashcat format) from NoteStore.sqlite.

* **warrant**: Tools used for preparing Apple warrant return data.
  * **download**: Downloads all .gpg files from an Apple-supplied .csv file.
  * **decrypt**: Decrypts all downloaded .gpg files from within a single diretory.

#### `hash`

Apply common hashing algorithms (MD5, SHA1, SHA256) to files.

## Examples

Below are some examples of possible commands:

**Bundle ID Lookup**
```bash
# command
digkit lookup bundleid -s apple com.toyopagroup.picaboo

# output
Snapchat
```

**ICCID Lookup**
```bash
# command
digkit lookup iccid 8981100022152967705

# output
Your SIM Card number, 8981100022152967705, uses ICCID format:

Major Industry Identifier (MII): 89 - Telecom - Private agency
International Calling Region: 81 - Japan
Issuer: 10 - NTT DOCOMO, INC.
Account Number: 002215296770
Checksum: 5
```

**Parsing NoteStore.sqlite**

```bash
# command
digkit parse database -d notestore -i NoteStore.sqlite -o . -f txt

# output
Saved TXT: ./notestore.txt
```

**File Hashing**

```bash
# command
digkit hash -a md5 -i file.txt

# output
MD5 (file.txt): 3e924496fd0105e8bbbb872030465995
```

## Notes

I plan to add the following features:
* IMEI lookup
* Cache.sqlite and knowledgeC.db parsers
* Apple warrant return parser
* comparitive hashing features
