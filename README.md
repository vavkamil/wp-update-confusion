# wp-update-confusion
WordPress Plugin Update Confusion

---

Simple tool to detect websites vulnerable to a novel supply chain attack targeting unclaimed WordPress plugins.

## Usage

```bash
$ pip install -r requirements.txt
$ python wp_update_confusion.py -h

 +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
 |W|o|r|d|P|r|e|s|s| |U|p|d|a|t|e| |C|o|n|f|u|s|i|o|n|
 +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+

usage: wp_update_confusion.py [-h] (-u URL | -l LIST) (-t | -p) [-o OUTPUT] [-s]

optional arguments:
  -h, --help     show this help message and exit
  -u URL         URL of WordPress site
  -l LIST        List of WordPress sites
  -t, --theme    Check themes
  -p, --plugins  Check plugins
  -o OUTPUT      Name of output file
  -s, --silent   Silent output

Have a nice day :)
```

## Example

```bash
$ python wp_update_confusion.py -p -u https://eng.*REDACTED*.com

 +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
 |W|o|r|d|P|r|e|s|s| |U|p|d|a|t|e| |C|o|n|f|u|s|i|o|n|
 +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+

-------------------------

[i] Target: https://eng.*REDACTED*.com

[i] Searching plugins

[i] Found WP plugin: revslider
	[i] Not vulnerable - heavily used

[i] Found WP plugin: fusion-core
	[i] Not vulnerable - heavily used

[i] Found WP plugin: xws
	[i] Not vulnerable - disallowed name

[i] Found WP plugin: *REDACTED*
	[?] Vulnerable to WP Plugin Confusion attack

	[!] https://newsroom.*REDACTED*.com/wp-content/plugins/*REDACTED*
	[!] https://wordpress.org/plugins/*REDACTED*

[i] Found WP plugin: solvmedias
	[i] Not vulnerable - already claimed
```
