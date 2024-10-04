#!/usr/bin/env python3

import requests
from github import Github
import shodan
import argparse
import os

# Tool details
TOOL_NAME = "AutoDork"
VERSION = "0.1"
DEVELOPER = "Developed by Jaseel"

# API Keys (Replace with your own)
SHODAN_API_KEY = "3llhwb3WazzNSamxKr8gWiDUtnjd2OuY"
GITHUB_API_KEY = ""
SERPAPI_KEY = "4e3cb5483676200d6665504c1042597549f9f9c206e9c68b59a6e8fcb5cf2f15"

# Initialize Shodan and GitHub
shodan_api = shodan.Shodan(SHODAN_API_KEY)
github_api = Github(GITHUB_API_KEY)

# Color helper for terminal output
def print_colored(text, color="default"):
    colors = {
        "default": "\033[0m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "blue": "\033[94m",
    }
    print(f"{colors.get(color, colors['default'])}{text}{colors['default']}")

# Subdomain Enumeration
def subdomain_enumeration(domain):
    subdomains = []
    try:
        response = requests.get(f"https://api.sublist3r.com/search.php?domain={domain}")
        subdomains = response.json()
    except Exception as e:
        print_colored(f"Error in subdomain enumeration: {e}", "red")
    return subdomains

# Google Dorking (using SerpAPI)
def google_dorking(dork_query):
    params = {
        "engine": "google",
        "q": dork_query,
        "api_key": SERPAPI_KEY
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        return response.json().get("organic_results", [])
    except Exception as e:
        print_colored(f"Error in Google Dorking: {e}", "red")
        return []

# GitHub Dorking
def github_dorking(query):
    try:
        results = github_api.search_code(query)
        return results
    except Exception as e:
        print_colored(f"Error in GitHub Dorking: {e}", "red")
        return []

# Shodan Dorking
def shodan_dorking(query):
    try:
        results = shodan_api.search(query)
        return results.get('matches', [])
    except shodan.APIError as e:
        print_colored(f"Error in Shodan Dorking: {e}", "red")
        return []

# Main function
def main():
    parser = argparse.ArgumentParser(description=f"{TOOL_NAME} - A dorking tool by {DEVELOPER}")
    parser.add_argument("--domain", help="Domain for subdomain enumeration", required=True)
    parser.add_argument("--google-dork", help="Google Dorking query", required=True)
    parser.add_argument("--github-dork", help="GitHub Dorking query (e.g., 'password')", required=True)
    parser.add_argument("--shodan-dork", help="Shodan Dorking query (e.g., 'Apache')", required=True)
    parser.add_argument("--version", action="version", version=f"{TOOL_NAME} {VERSION}")
    
    args = parser.parse_args()

    print_colored(f"\n[+] {TOOL_NAME} {VERSION} - {DEVELOPER}\n", "blue")

    # Subdomain Enumeration
    print_colored("\n[+] Starting Subdomain Enumeration...", "yellow")
    subdomains = subdomain_enumeration(args.domain)
    if subdomains:
        print_colored("[+] Subdomains found:", "green")
        for sub in subdomains:
            print(f"- {sub}")

    # Google Dorking
    print_colored("\n[+] Starting Google Dorking...", "yellow")
    google_results = google_dorking(args.google_dork)
    if google_results:
        print_colored("[+] Google Dorking results:", "green")
        for result in google_results:
            print(f"- {result.get('title')}: {result.get('link')}")

    # GitHub Dorking
    print_colored("\n[+] Starting GitHub Dorking...", "yellow")
    github_results = github_dorking(args.github_dork)
    if github_results:
        print_colored("[+] GitHub Dorking results:", "green")
        for result in github_results:
            print(f"- {result.repository.full_name}: {result.html_url}")

    # Shodan Dorking
    print_colored("\n[+] Starting Shodan Dorking...", "yellow")
    shodan_results = shodan_dorking(args.shodan_dork)
    if shodan_results:
        print_colored("[+] Shodan Dorking results:", "green")
        for result in shodan_results:
            print(f"- IP: {result['ip_str']} | Port: {result['port']}")

if __name__ == "__main__":
    main()
