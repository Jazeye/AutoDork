import requests
import argparse

# Constants for API keys
RAPIDAPI_KEY = "1d256ab7f5mshf4e099388517e7dp1966ddjsn0af7bb19ba17 "  # Replace with your RapidAPI key
GITHUB_API_KEY = "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"  # Replace with your GitHub API key
SERPAPI_KEY = "4e3cb5483676200d6665504c1042597549f9f9c206e9c68b59a6e8fcb5cf2f15"  # Replace with your SerpAPI key


# Tool Information
TOOL_NAME = "AutoDork"
TOOL_VERSION = "0.1"
DEVELOPER = "Jaseel"

# Function to print colored output
def print_colored(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "end": "\033[0m",
    }
    print(f"{colors[color]}{message}{colors['end']}")

# Function to print the ASCII banner
def print_banner():
    banner = rf"""
                _        _____             _    
     /\        | |      |  __ \           | |   
    /  \  _   _| |_ ___ | |  | | ___  _ __| | __
   / /\ \| | | | __/ _ \| |  | |/ _ \| '__| |/ /
  / ____ \ |_| | || (_) | |__| | (_) | |  |   < 
 /_/    \_\__,_|\__\___/|_____/ \___/|_|  |_|\_\
                                                    
                v{TOOL_VERSION} by {DEVELOPER}
    """
    print_colored(banner, "green")

# Subdomain Enumeration using RapidAPI
def subdomain_enumeration(domain):
    url = f"https://subdomain-scan1.p.rapidapi.com/?domain={domain}"
    headers = {
        "x-rapidapi-host": "subdomain-scan1.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Check if data is a list
            if isinstance(data, list):
                return data  # If data is a list, return it directly
            else:
                print_colored("Unexpected response format: expected a list.", "red")
                return []
        else:
            print_colored(f"Error in subdomain enumeration: {response.text}", "red")
            return []
    except Exception as e:
        print_colored(f"Error in subdomain enumeration: {e}", "red")
        return []

# Google Dorking
def google_dorking(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract and return search results
            results = data.get("organic_results", [])
            return [result.get("link") for result in results if "link" in result]
        else:
            print_colored(f"Error in Google Dorking: {response.text}", "red")
            return []
    except Exception as e:
        print_colored(f"Error in Google Dorking: {e}", "red")
        return []

# GitHub Dorking
def github_dorking(query):
    url = f"https://api.github.com/search/code?q={query}"
    headers = {
        "Authorization": f"token {GITHUB_API_KEY}",  # Use the Authorization header
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Extract and return repository URLs
            return [item["html_url"] for item in data.get("items", [])]
        else:
            print_colored(f"Error in GitHub Dorking: {response.text}", "red")
            return []
    except Exception as e:
        print_colored(f"Error in GitHub Dorking: {e}", "red")
        return []

# Main function
def main():
    print_banner()  # Print the ASCII banner

    parser = argparse.ArgumentParser(description="Autodork Tool")
    parser.add_argument("--domain", type=str, required=True, help="Domain to enumerate subdomains.")
    parser.add_argument("--google-dork", type=str, required=False, help="Google dork query.")
    parser.add_argument("--github-dork", type=str, required=False, help="GitHub dork query.")

    args = parser.parse_args()

    # Subdomain enumeration
    print_colored(f"Enumerating subdomains for: {args.domain}", "blue")
    subdomains = subdomain_enumeration(args.domain)
    print_colored("Subdomains found:", "yellow")
    for sub in subdomains:
        print(f" - {sub}")

    # Google Dorking
    if args.google_dork:
        print_colored(f"Running Google Dork: {args.google_dork}", "blue")
        google_results = google_dorking(args.google_dork)
        print_colored("Google Dork Results:", "yellow")
        for link in google_results:
            print(f" - {link}")

    # GitHub Dorking
    if args.github_dork:
        print_colored(f"Running GitHub Dork: {args.github_dork}", "blue")
        github_results = github_dorking(args.github_dork)
        print_colored("GitHub Dork Results:", "yellow")
        for link in github_results:
            print(f" - {link}")

if __name__ == "__main__":
    main()
