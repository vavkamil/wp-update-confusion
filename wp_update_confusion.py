#!/usr/bin/env python3

import os
import re
import sys
import json
import argparse
import requests


def banner():
    banner = "\n"
    banner += " +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+\n"
    banner += " |W|o|r|d|P|r|e|s|s| |U|p|d|a|t|e| |C|o|n|f|u|s|i|o|n|\n"
    banner += " +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+\n"

    return banner


def parse_args():
    parser = argparse.ArgumentParser(
        description="",
        epilog="Have a nice day :)",
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("-u", dest="url", help="URL of WordPress site")
    target.add_argument("-l", dest="list", help="List of WordPress sites")
    check = parser.add_mutually_exclusive_group(required=True)
    check.add_argument(
        "-t", "--theme", dest="theme", action="store_true", help="Check themes"
    )
    check.add_argument(
        "-p", "--plugins", dest="plugins", action="store_true", help="Check plugins"
    )
    parser.add_argument("-o", dest="output", help="Name of output file")
    parser.add_argument(
        "-s", "--silent", dest="silent", action="store_true", help="Silent output"
    )

    return parser.parse_args()


def detect_theme(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    }

    try:
        res = requests.get(
            url,
            headers=headers,
        )
    except:
        return 0

    html = res.text

    match = re.search("wp-content/themes/(.*?)/", html)

    try:
        theme = match.group(1)
    except:
        theme = False

    return theme


def detect_plugins(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    }

    try:
        res = requests.get(url, headers=headers, timeout=5)
    except:
        return 0

    html = res.text

    match = re.findall("wp-content/plugins/(.*?)/", html)
    plugins = list(set(match))

    return plugins


def check_wordpress_org_theme(theme):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    }

    res = requests.get(
        f"https://wordpress.org/themes/{theme}",
        headers=headers,
    )

    if res.status_code == 404:
        is_vulnerable = True
    else:
        is_vulnerable = False

    return is_vulnerable


def check_wordpress_org_plugin(plugin):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    }

    res = requests.get(
        f"https://plugins.svn.wordpress.org/{plugin}/",
        headers=headers,
    )

    if res.status_code == 404:
        is_vulnerable = True
    else:
        is_vulnerable = False

    return is_vulnerable


def check_paid_plugins(plugin):
    f = open("paid_plugins.json")

    paid_plugins = json.load(f)

    f.close()

    if plugin in paid_plugins:
        return 1
    else:
        return 0


def check_active_installs(plugin):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    }

    res = requests.get(
        f"https://api.wordpress.org/stats/plugin/1.0/downloads.php?slug={plugin}&historical_summary=1",
        headers=headers,
    )

    downloads = res.json()["all_time"]

    if downloads and int(downloads) > 100:
        return 0
    else:
        return 1


def is_allowed_slug(plugin):
    # https://meta.trac.wordpress.org/ticket/5868
    # https://meta.trac.wordpress.org/browser/sites/trunk/wordpress.org/public_html/wp-content/plugins/plugin-directory/shortcodes/class-upload-handler.php

    # has_reserved_slug()
    reserved_slug = [
        "about",
        "admin",
        "browse",
        "category",
        "developers",
        "developer",
        "featured",
        "filter",
        "new",
        "page",
        "plugins",
        "popular",
        "post",
        "search",
        "tag",
        "updated",
        "upload",
        "wp-admin",
        "jquery",
        "wordpress",
        "akismet-anti-spam",
        "site-kit-by-google",
        "yoast-seo",
        "woo",
        "wp-media-folder",
        "wp-file-download",
        "wp-table-manager",
    ]

    # has_trademarked_slug()
    trademarked_slug = [
        "adobe-",
        "adsense-",
        "advanced-custom-fields-",
        "adwords-",
        "akismet-",
        "all-in-one-wp-migration",
        "amazon-",
        "android-",
        "apple-",
        "applenews-",
        "aws-",
        "bbpress-",
        "bing-",
        "bootstrap-",
        "buddypress-",
        "contact-form-7-",
        "cpanel-",
        "disqus-",
        "divi-",
        "dropbox-",
        "easy-digital-downloads-",
        "elementor-",
        "envato-",
        "fbook",
        "facebook",
        "fb-",
        "fb-messenger",
        "fedex-",
        "feedburner",
        "ganalytics-",
        "gberg",
        "github-",
        "givewp-",
        "google-",
        "googlebot-",
        "googles-",
        "gravity-form-",
        "gravity-forms-",
        "gutenberg",
        "guten-",
        "hubspot-",
        "ig-",
        "insta-",
        "instagram",
        "internet-explorer-",
        "jetpack-",
        "macintosh-",
        "mailchimp-",
        "microsoft-",
        "ninja-forms-",
        "oculus",
        "onlyfans-",
        "only-fans-",
        "paddle-",
        "paypal-",
        "pinterest-",
        "stripe-",
        "tiktok-",
        "trustpilot",
        "twitter-",
        "tweet",
        "ups-",
        "usps-",
        "vvhatsapp",
        "vvcommerce",
        "vva-",
        "vvoo",
        "wa-",
        "wh4tsapps",
        "whatsapp",
        "whats-app",
        "watson",
        "windows-",
        "wocommerce",
        "woocom-",
        "woocommerce",
        "woocomerce",
        "woo-commerce",
        "woo-",
        "wo-",
        "wordpress",
        "wordpess",
        "wpress",
        "wp-",
        "wp-mail-smtp-",
        "yahoo-",
        "yoast",
        "youtube-",
    ]

    # Check allowed characters
    if not re.match("^[a-z0-9-]*$", plugin):
        return 0

    # Prevent short plugin names (they're generally SEO grabs).
    if len(plugin) < 5:
        return 0

    # Check if forbidden slug
    if plugin in reserved_slug:
        return 0

    # Check if trademarked slug
    for trademark in trademarked_slug:
        # Trademarks ending in "-" indicate slug cannot begin with that term.
        if trademark.endswith("-"):
            if plugin.startswith(trademark):
                return 0
        # Otherwise, the term cannot appear anywhere in slug.
        # check for 'for-TRADEMARK' exceptions.
        elif trademark in plugin and not plugin.endswith(f"for-{trademark}"):
            return 0

    return 1


def main(args):

    urls = []

    if args.silent:
        sys.stdout = open(os.devnull, "a")
        sys.stderr = open(os.devnull, "a")

    if args.list:
        with open(args.list) as file:
            while (url := file.readline().rstrip()) :
                urls.append(url)
    else:
        urls.append(args.url)

    for url in urls:
        vulnerable = []
        print("-------------------------\n")
        print(f"[i] Target: {url}\n")

        if args.theme:
            print("[i] Searching theme\n")

            theme = detect_theme(url)
            if theme:
                print(f"[i] Found WP theme: {theme}\n")

                is_vulnerable = check_wordpress_org_theme(theme)
                if is_vulnerable:
                    print("\t[!] Vulnerable to WP Theme Confusion attack\n")
                    print(f"\t[!] {url}/wp-content/themes/{theme}")
                    print(f"\t[!] https://wordpress.org/themes/{theme}\n")
                    vulnerable.append(f"{url}/wp-content/themes/{theme}")
                else:
                    print(f"\t[i] Not vulnerable\n")

        if args.plugins:
            print(f"[i] Searching plugins\n")
            plugins = detect_plugins(url)

            for plugin in plugins or []:
                print(f"[i] Found WP plugin: {plugin}")

                is_allowed = is_allowed_slug(plugin)
                if not (is_allowed):
                    print(f"\t[i] Not vulnerable - disallowed name\n")
                    continue

                # if (plugin.endswith("-pro") or plugin.endswith("-premium")):
                #     with open("paid.txt", "a") as f:
                #         f.write("%s\n" % plugin)
                #     f.close()
                #     print(f"\t[i] Not vulnerable - pro/premium plugin\n")
                #     continue

                # is_paid = check_paid_plugins(plugin)
                # if(is_paid):
                #     print(f"\t[i] Not vulnerable - paid plugin\n")
                #     continue

                is_vulnerable = check_wordpress_org_plugin(plugin)
                if is_vulnerable:
                    is_not_used = check_active_installs(plugin)
                    if not (is_not_used):
                        print(f"\t[i] Not vulnerable - heavily used\n")
                        continue
                    print("\t[?] Vulnerable to WP Plugin Confusion attack\n")
                    print(f"\t[!] {url}/wp-content/plugins/{plugin}")
                    print(f"\t[!] https://wordpress.org/plugins/{plugin}\n")
                    vulnerable.append(f"{url}/wp-content/plugins/{plugin}")
                else:
                    print(f"\t[i] Not vulnerable - already claimed\n")

        if args.output:
            if vulnerable:
                with open(args.output, "a") as f:
                    for item in vulnerable:
                        f.write("%s\n" % item)
                f.close()


if __name__ == "__main__":
    print(banner())
    args = parse_args()
    main(args)
