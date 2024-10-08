# AutoDork

A Python tool for automated dorking using GitHub, SerpAPI, and RapidAPI.

## Installation & Setup

### 1. **Clone the Repository**

```bash

git clone <url_of_the_repository>
cd AutoDork

```

### 2. **Create and Activate a Virtual Environment**

To keep dependencies isolated, it's recommended to use a virtual environment:

```bash

python3 -m venv venv
source venv/bin/activate

```

### 3. **Install Required Python Packages**

Ensure `pip` is installed on your machine. Install the necessary packages:

```bash

sudo apt update
sudo apt install python3-pip
pip install requests argparse

```

### 4. **Set Up API Keys**

### 1. **GitHub API Key**

1. Go to [GitHub](https://github.com/) and log in.
2. Navigate to **Settings** > **Developer settings** > **Personal access tokens**.
3. Click **Generate new token** and select the following permissions:
    - `repo`
    - `read:org`
    - `read:user`
    - `public_repo`
4. Copy and save your token.

### 2. **SerpAPI Key**

1. Sign up at [SerpAPI](https://serpapi.com/).
2. Find your API key in the **Dashboard** under **API Key**.
3. Copy and save your key.

### 3. **RapidAPI Key**

1. Sign up at [RapidAPI](https://rapidapi.com/).
2. On the **API Marketplace**, find the API **Subdomain Scan** .
3. Locate your API key on the API's **Endpoints** or **Pricing** page.
4. See the API key in the left sidebar. Also, don't forget to purchase the API if required. 

### 5. **Configure the Tool**

Edit the script to add your API keys:

```python

RAPIDAPI_KEY = "your_actual_RAPIDAPI_key"  
GITHUB_API_KEY = "your_actual_github_api_key"
SERPAPI_KEY = "your_actual_serpapi_key"

```

### 6. **Run the Script**

After setting up the API keys and installing the required modules, run the script:

```bash

python3 autodork.py

example : python3 autodork.py --domain example.com --google-dork "site:example.com inurl:admin" --github-dork "password filename:.env"

```

## Notes

- **API Rate Limits**: Keep track of rate limits for each API to avoid being blocked.
- **Sensitive Information**: Do not share API keys publicly. Store them in environment variables or use secret management tools for better security.
- **Error Handling**: Consider adding error handling to manage API errors or rate limits effectively
