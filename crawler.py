#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from lib.cli.Client import Client

# Argument parsing initialization
parser = argparse.ArgumentParser(description="Scrap GitHub data.")
parser.add_argument("url", help="URL of the GitHub repository or user profile")
parser.add_argument("-u", "--username", help="GitHub name", default=None)
parser.add_argument("-p", "--password", help="GitHub password", default=None)
args = parser.parse_args()

if __name__ == '__main__':
    cli = Client(args.username, args.password)
    cli.main(args.url)
