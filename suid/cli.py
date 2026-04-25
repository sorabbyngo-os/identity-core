#!/usr/bin/env python3
"""
suid-cli — Sorabbyngo Universal ID command-line tool
Operators and IT staff use this for ID generation,
validation, forensic extraction, and tamper detection.

Usage:
    suid generate PAT KE045
    suid validate PAT-20260421-KE045-A3X9KM-7F
    suid parse PAT-20260421-KE045-A3X9KM-7F
    suid forensic PAT-20260421-KE045-A3X9KM-7F
    suid batch PAT KE045 --count 10
    suid tamper-check PAT-... DOC-... TXN-...
    suid prefixes
    suid regions --country Kenya
"""
import argparse
import json
import sys

from suid.generator import SUID
from suid.validator import validate, is_tampered
from suid.registry.prefixes import PREFIX
from suid.forensics.extractor import ForensicExtractor
from suid.regions.africa import ALL_REGIONS as AFRICA_REGIONS


def cmd_generate(args):
    prefix = args.prefix.upper()
    region = args.region.upper()
    try:
        suid = SUID.generate(prefix, region)
        print(suid)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_validate(args):
    for suid in args.suids:
        ok  = validate(suid, verify_checksum=True)
        tam = is_tampered(suid) if ok else False
        status = "VALID" if ok else "INVALID"
        tamper = " ⚠️  TAMPERED" if tam else ""
        print(f"  {status}{tamper}  {suid}")
    sys.exit(0 if all(validate(s, verify_checksum=True) for s in args.suids) else 1)


def cmd_parse(args):
    result = SUID.parse(args.suid)
    print(json.dumps(result, indent=2))


def cmd_forensic(args):
    report = ForensicExtractor.entity_report(args.suid)
    print(json.dumps(report, indent=2, default=str))


def cmd_batch(args):
    suids = SUID.batch(args.prefix.upper(), args.region.upper(), args.count)
    for s in suids:
        print(s)


def cmd_tamper_check(args):
    tampered = ForensicExtractor.detect_tampered(args.suids)
    if tampered:
        print(f"⚠️  {len(tampered)} TAMPERED ID(s) detected:")
        for s in tampered:
            print(f"  {s}")
        sys.exit(2)
    else:
        print(f"✓ All {len(args.suids)} IDs pass checksum verification")


def cmd_prefixes(args):
    domains = PREFIX.by_domain()
    for domain, codes in domains.items():
        print(f"\n{domain.upper().replace('_', ' ')}:")
        for code in codes:
            print(f"  {code}  {PREFIX.describe(code)}")


def cmd_regions(args):
    country_filter = args.country.lower() if args.country else None
    for code, info in AFRICA_REGIONS.items():
        if country_filter and info["country"].lower() != country_filter:
            continue
        print(f"  {code}  {info['name']}, {info['country']}")


def cmd_law_enforcement(args):
    report = ForensicExtractor.law_enforcement_summary(
        suids=args.suids,
        case_number=args.case or "",
        requesting_authority=args.authority or "",
        authorized_by=args.authorized_by or "",
    )
    print(json.dumps(report, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(
        prog="suid",
        description="Sorabbyngo Universal ID — command-line tool",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # generate
    p = sub.add_parser("generate", help="Generate a new SUID")
    p.add_argument("prefix", help="Entity type prefix (e.g. PAT, DOC, TXN)")
    p.add_argument("region", nargs="?", default="KE047",
                   help="Region code (default: KE047 Nairobi)")

    # validate
    p = sub.add_parser("validate", help="Validate one or more SUIDs")
    p.add_argument("suids", nargs="+", help="SUID(s) to validate")

    # parse
    p = sub.add_parser("parse", help="Parse a SUID into its components")
    p.add_argument("suid", help="SUID to parse")

    # forensic
    p = sub.add_parser("forensic", help="Generate forensic report for a SUID")
    p.add_argument("suid", help="SUID to analyze")

    # batch
    p = sub.add_parser("batch", help="Generate multiple SUIDs")
    p.add_argument("prefix", help="Entity type prefix")
    p.add_argument("region", nargs="?", default="KE047")
    p.add_argument("--count", type=int, default=10)

    # tamper-check
    p = sub.add_parser("tamper-check", help="Check SUIDs for tampering")
    p.add_argument("suids", nargs="+")

    # prefixes
    sub.add_parser("prefixes", help="List all registered entity prefixes")

    # regions
    p = sub.add_parser("regions", help="List supported African regions")
    p.add_argument("--country", help="Filter by country name")

    # law-enforcement
    p = sub.add_parser("law-enforcement", help="Generate law enforcement report")
    p.add_argument("suids", nargs="+")
    p.add_argument("--case", help="Case number")
    p.add_argument("--authority", help="Requesting authority")
    p.add_argument("--authorized-by", dest="authorized_by")

    args = parser.parse_args()

    commands = {
        "generate":        cmd_generate,
        "validate":        cmd_validate,
        "parse":           cmd_parse,
        "forensic":        cmd_forensic,
        "batch":           cmd_batch,
        "tamper-check":    cmd_tamper_check,
        "prefixes":        cmd_prefixes,
        "regions":         cmd_regions,
        "law-enforcement": cmd_law_enforcement,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
