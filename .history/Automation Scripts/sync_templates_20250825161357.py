# Upwork System/Automation Scripts/DataIngest/upwork.py
# FINAL PRODUCTION VERSION - Scrapes a job feed URL for recent job links and processes them.
import argparse
import json
import re
import time
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlparse
import sys
import os

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# --- Configuration ---
OUTPUT_DIR = Path(__file__).parent / "job_outputs"
AUTOMATION_PROFILE_DIR = Path(__file__).parent / "chrome_profile_automation"
SETUP_MARKER_FILE = AUTOMATION_PROFILE_DIR / "setup_complete.marker"
# **FIX: BASE_URL is now correctly defined at the top level.**
BASE_URL = "https://www.upwork.com/nx/find-work/"

# --- Helper Functions for Parsing ---
def get_text_safe(element, selector):
    """Safely finds an element by selector and returns its stripped text, or None."""
    if not element: return None
    found = element.select_one(selector)
    return found.get_text(strip=True) if found else None

def convert_spent_to_number(spent_str):
    """Converts client spend string like '$21K+' or '$500+' to a number."""
    if not spent_str: return 0
    spent_str = spent_str.lower().replace('$', '').replace('+', '').strip()
    if 'k' in spent_str: ret