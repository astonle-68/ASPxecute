#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Process shellcode file and optional metadata (class, namespace, extension).",
    )

    parser.add_argument("-s", "--shellcode", help="Path to shellcode file", required=True)
    parser.add_argument("-c", "--class", dest="classname", help="Name of Class (optional).", required=False)
    parser.add_argument("-n", "--namespace", help="Name of Namespace", required=False)
    parser.add_argument("-e", "--extension", default="wkdb", help="Extension name to use (default: %(default)s).", required=False)

    return parser.parse_args()
