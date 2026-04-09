"""
MnemonicTriage — BIP-39 Forensic Phrase Validator
---------------------------------------------------
Validates BIP-39 mnemonic phrases against the official wordlist and checksum.
Intended for forensic triage use — does NOT derive keys or connect to networks.

Usage:
    python mnemonic_triage.py "word1 word2 ... word12"
    python mnemonic_triage.py  # interactive prompt
"""

import sys
import json
import argparse
from mnemonic import Mnemonic


SUPPORTED_LANGUAGES = [
    "english", "spanish", "french", "italian",
    "portuguese", "czech", "japanese", "korean", "chinese_simplified"
]


def validate_bip39(phrase: str, language: str = "english") -> dict:
    """
    Validates a BIP-39 mnemonic phrase.

    Parameters
    ----------
    phrase   : The mnemonic phrase string to validate.
    language : BIP-39 wordlist language (default: english).

    Returns
    -------
    dict with validation results. Does NOT derive keys or addresses.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language '{language}'. Choose from: {SUPPORTED_LANGUAGES}")

    mnemo = Mnemonic(language)
    phrase = phrase.strip().lower()
    words = phrase.split()

    wordlist = set(mnemo.wordlist)
    invalid_words = [w for w in words if w not in wordlist]

    valid_word_count = len(words) in [12, 15, 18, 21, 24]
    all_in_wordlist = len(invalid_words) == 0

    checksum_valid = False
    if valid_word_count and all_in_wordlist:
        checksum_valid = mnemo.check(phrase)

    return {
        "word_count": len(words),
        "valid_word_count": valid_word_count,
        "all_words_in_wordlist": all_in_wordlist,
        "invalid_words": invalid_words,
        "checksum_valid": checksum_valid,
        "is_valid_bip39": valid_word_count and all_in_wordlist and checksum_valid,
        "language": language,
    }


def print_report(result: dict, phrase: str = "") -> None:
    """Prints a human-readable validation report."""
    ok = "✓"
    fail = "✗"

    print("\n" + "=" * 40)
    print("  MnemonicTriage — BIP-39 Validation Report")
    print("=" * 40)
    print(f"  Language         : {result['language']}")
    print(f"  Word count       : {result['word_count']}  "
          f"{'(' + ok + ' valid length)' if result['valid_word_count'] else '(' + fail + ' must be 12/15/18/21/24)'}")
    print(f"  Words in list    : {ok if result['all_words_in_wordlist'] else fail}")
    if result["invalid_words"]:
        print(f"  Invalid words    : {', '.join(result['invalid_words'])}")
    print(f"  Checksum valid   : {ok if result['checksum_valid'] else fail}")
    print("-" * 40)
    verdict = f"  VALID BIP-39 {ok}" if result["is_valid_bip39"] else f"  INVALID BIP-39 {fail}"
    print(verdict)
    print("=" * 40 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="MnemonicTriage — BIP-39 mnemonic phrase validator for forensic triage."
    )
    parser.add_argument(
        "phrase",
        nargs="*",
        help="Mnemonic phrase words (or omit for interactive prompt)."
    )
    parser.add_argument(
        "--language", "-l",
        default="english",
        choices=SUPPORTED_LANGUAGES,
        help="BIP-39 wordlist language (default: english)."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON."
    )
    parser.add_argument(
        "--batch", "-b",
        metavar="FILE",
        help="Validate multiple phrases from a file (one phrase per line)."
    )

    args = parser.parse_args()

    # Batch mode
    if args.batch:
        try:
            with open(args.batch, "r") as f:
                phrases = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{args.batch}' not found.")
            sys.exit(1)

        results = []
        for phrase in phrases:
            result = validate_bip39(phrase, args.language)
            results.append(result)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Phrase: {phrase[:30]}{'...' if len(phrase) > 30 else ''}")
                print_report(result)
        return

    # Single phrase mode
    if args.phrase:
        phrase = " ".join(args.phrase)
    else:
        phrase = input("Enter mnemonic phrase: ").strip()

    if not phrase:
        print("No phrase provided.")
        sys.exit(1)

    result = validate_bip39(phrase, args.language)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)

    sys.exit(0 if result["is_valid_bip39"] else 1)


if __name__ == "__main__":
    main()
