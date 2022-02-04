# CloudTwifier

## What is it
This program will fetch Tweets from a given query or hashtag and generate a word cloud of the most frequently used words associated to your query.

## Requirements
Install requirements with `pip install -r requirements.txt`

Note: This program requires an API BEARER_TOKEN. Once you obtain it, place it in `auth.py`.
<br />
More info at [developer.twitter.com](https://developer.twitter.com/).


## How to use it
```
cloudtwifier.py [-h] [-q QUERY] [-r] [-o OUTPUT] [--quiet]
```
Short | Argument | Info
---|---|---
`-h` | `--help` | show this help message and exit
`-q QUERY` | `--query QUERY` | Search by specified query
`-r` | `--retweets` | Include retweets
`-o OUTPUT` | `--output OUTPUT` | Specify output directory
/ | `--quiet` | Disable verbosity

## Contributions
Contributions are welcome, feel free to submit issues and/or pull requests.

### To-Do
- Add 'Search by Country'

### Known issues
- None

## LICENSE

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

"CloudTwifier" - Generate word clouds based on Twitter content.<br />
Copyright (C) 2022 Andrea Varesio <https://www.andreavaresio.com/>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a [copy of the GNU General Public License](https://github.com/andrea-varesio/CloudTwifier/blob/main/LICENSE)
along with this program.  If not, see <https://www.gnu.org/licenses/>.

<div align="center">
<a href="https://github.com/andrea-varesio/CloudTwifier/">
  <img src="http://hits.dwyl.com/andrea-varesio/CloudTwifier.svg?style=flat-square" alt="Hit count" />
</a>
</div>
