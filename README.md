# MnemonicTriage
Forensic triage tool for validating BIP-39 cryptocurrency mnemonic phrases. Wordlist + checksum validation only — no key derivation, no network access. Supports 9 languages and batch mode.

## Intended Use

This tool is designed for **digital forensic examiners and law enforcement** to quickly determine whether a phrase already in their possession constitutes a valid BIP-39 mnemonic — useful for triaging evidence on-scene or in the lab.

> ⚠️ **MnemonicTriage does NOT derive wallet addresses, private keys, or balances.** It only validates whether a given phrase conforms to the BIP-39 standard.

## Features

- Validates word count (12, 15, 18, 21, or 24 words)
- Checks all words against the official BIP-39 wordlist
- Verifies embedded checksum
- Supports 9 languages
- JSON output for integration with other forensic tools
- Batch mode for validating multiple phrases from a file

## Installation

```bash
git clone https://github.com/your-org/MnemonicTriage.git
cd MnemonicTriage
pip install -r requirements.txt
```

## Usage

### Single phrase (interactive)
```bash
python mnemonic_triage.py
```

### Single phrase (argument)
```bash
python mnemonic_triage.py "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
```

### JSON output
```bash
python mnemonic_triage.py "word1 ... word12" --json
```

### Non-English wordlist
```bash
python mnemonic_triage.py "word1 ... word12" --language spanish
```

Supported languages: `english`, `spanish`, `french`, `italian`, `portuguese`, `czech`, `japanese`, `korean`, `chinese_simplified`

### Batch mode (one phrase per line)
```bash
python mnemonic_triage.py --batch phrases.txt
```

### Exit codes
| Code | Meaning |
|------|---------|
| `0`  | Valid BIP-39 phrase |
| `1`  | Invalid phrase |

## Example Output

```
========================================
  MnemonicTriage — BIP-39 Validation Report
========================================
  Language         : english
  Word count       : 12  (✓ valid length)
  Words in list    : ✓
  Checksum valid   : ✓
----------------------------------------
  VALID BIP-39 ✓
========================================
```

## Legal & Ethical Notice

MnemonicTriage is intended solely for lawful forensic examination of evidence obtained through proper legal authority (warrant, consent, etc.). Misuse to access wallets without authorization may violate computer fraud, theft, and wiretapping laws.

## License

MIT License — see [LICENSE](LICENSE)

