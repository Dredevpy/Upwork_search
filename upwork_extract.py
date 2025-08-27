import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import json
import time

# Google Sheets Setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  # your Google API service account credentials
SHEET_NAME = "UpworkJobs"        # sheet name containing job URLs

def get_sheet_urls():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    urls = sheet.col_values(1)  # assumes first column contains job URLs
    return [u for u in urls if u.startswith("http")]

def scrape_job(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return {"error": f"Failed to fetch {url}"}

    soup = BeautifulSoup(r.text, "html.parser")
    data = {"url": url}

    # Extract basic info
    title = soup.find("h1")
    data["title"] = title.get_text(strip=True) if title else None

    budget = soup.find("span", {"data-test": "job-type"})
    data["job_type"] = budget.get_text(strip=True) if budget else None

    rate = soup.find("strong")
    data["budget_or_rate"] = rate.get_text(strip=True) if rate else None

    description = soup.find("div", {"data-test": "job-description-text"})
    data["description"] = description.get_text(" ", strip=True) if description else None

    skills = soup.find_all("span", {"data-test": "token"})
    data["skills"] = [s.get_text(strip=True) for s in skills]

    applicants = soup.find("strong", string=lambda t: t and "applicants" in t.lower())
    data["applicants"] = applicants.get_text(strip=True) if applicants else None

    client = soup.find("div", {"data-test": "client-info"})
    data["client_info"] = client.get_text(" ", strip=True) if client else None

    return data

def main():
    urls = get_sheet_urls()
    all_jobs = []
    for url in urls:
        print(f"Scraping {url} ...")
        job_data = scrape_job(url)
        all_jobs.append(job_data)
        time.sleep(2)  # avoid rate limits

    with open("upwork_job.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)

    print("Saved results to upwork_job.json")

if __name__ == "__main__":
    main()
