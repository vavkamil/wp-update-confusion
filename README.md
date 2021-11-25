# WordPress Plugin Update Confusion

Simple tool to detect websites vulnerable to a novel supply chain attack targeting unclaimed WordPress plugins.

Read more:
- [https://vavkamil.cz/2021/11/25/wordpress-plugin-confusion-update-can-get-you-pwned/](https://vavkamil.cz/2021/11/25/wordpress-plugin-confusion-update-can-get-you-pwned/)
- [https://galnagli.com/Wordpress_Plugin_Update_Confusion/](https://galnagli.com/Wordpress_Plugin_Update_Confusion/)

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

## Nuclei template

The nuclei engine has its limitations, but with some pipe hacks and `jq`, one can scan a list of targets. It will result in a ton of false positives but will be much faster. See the [template](wp-update-confusion.yaml) and usage:

```
$ chaos -d u**r.com -bbq -http-url --silent | nuclei -t wp-update-confusion.yaml -json | jq -r '"https://plugins.svn.wordpress.org/" + .["extracted-results"][] + "/?" + .["matched-at"]' | httpx -silent -random-agent -mc 404

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   2.5.3

		projectdiscovery.io

[WRN] Use with caution. You are responsible for your actions.
[WRN] Developers assume no liability and are not responsible for any misuse or damage.
[INF] Using Nuclei Engine 2.5.3 (latest)
[INF] Using Nuclei Templates 8.6.1 (latest)
[INF] Using Interactsh Server https://interactsh.com
[INF] Templates added in last update: 44
[INF] Templates loaded for scan: 1
https://plugins.svn.wordpress.org/td-standard-pack/?https://eng.u**r.com/
https://plugins.svn.wordpress.org/u**r-eng-regional-plugins/?https://eng.u**r.com/
https://plugins.svn.wordpress.org/td-cloud-library/?https://eng.u**r.com/
https://plugins.svn.wordpress.org/search-filter-pro/?https://eng.u**r.com/
```


## False Positives

```
- ie-sitemode
- miniorange
- Everything with -pro appended
```
