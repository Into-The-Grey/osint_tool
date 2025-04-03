#!/usr/bin/env python3
import argparse
from controller import Controller
from config import load_config

def parse_args():
    parser = argparse.ArgumentParser(description="Python OSINT Tool (CLI mode)")
    parser.add_argument(
        '-t', '--target',
        action='append',
        required=True,
        help="Input target (e.g., email:john.doe@example.com, username:jdoe, domain:example.com, ip:1.2.3.4, phone:+1234567890, address:123 Main St, realname:John Doe)"
    )
    parser.add_argument('--darkweb', action='store_true', help="Enable dark web scanning via Tor")
    parser.add_argument('--permutations', action='store_true', help="Enable username permutation search")
    parser.add_argument('--output', default="results.json", help="Output file (JSON format)")
    parser.add_argument('--host', help="Host for web UI (if not provided, runs in CLI mode)")
    parser.add_argument('--port', type=int, default=5000, help="Port for web UI")
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args)
    controller = Controller(config)
    controller.run(args.target)

if __name__ == '__main__':
    main()
