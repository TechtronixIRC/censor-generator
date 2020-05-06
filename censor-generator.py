#!/usr/bin/env python3
"""
Generate a censor configuration for InspIRCd

Copyright (c) 2020 Michael Hazell <michaelhazell@hotmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import requests

parser = argparse.ArgumentParser(
    description='Generate a censor.conf file for InspIRCd')
parser.add_argument('-o', '--output', type=str, default='censor.conf',
                    help='Output file, where the configuration will be written')
parser.add_argument('-r', '--replace', type=str, default='<censored>',
                    help='Replacement string for censored words')
parser.add_argument('-u', '--url', type=str,
                    default='', help='URL of the word list')
args = parser.parse_args()

def main():
    # Check to see if a URL was provided. Bail if not.
    if len(args.url) is 0:
        parser.print_help()
        print('[error] Word list URL missing. Please provide a URL that serves a plaintext list.')
        return

    # Print out the configuration that will be used, as a courtesy
    print(f'[config] Using {args.output} as output file')
    print(f'[config] Using {args.replace} as replacement string for censored words')
    print(f'[config] Using {args.url} as wordlist source')

    # This is actually the meat and potatoes
    response = requests.get(args.url)
    output = open(args.output, 'w')
    output.write('# censor.conf auto-generated by censor-generator.py\n')
    output.write('# Source available at https://www.techtronix.net\n')
    for word in response.iter_lines(decode_unicode=True):
        line = f'<badword text="{word}" replace="{args.replace}">\n'
        output.write(line)
    output.close()
    print(f'Done, output written to {args.output}')

if __name__ == "__main__":
    main()
