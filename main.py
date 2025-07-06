import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import tempfile
import time
import os

# Load environment variables
load_dotenv()
USERNAME = os.getenv("LINKEDIN_USERNAME")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Setup headless Chrome with safe options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Use a unique temporary user-data-dir to avoid SessionNotCreatedException
user_data_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# List of companies
companies = [
    # Major Investment Banks & Asset Managers
    "HSBC", "BNP Paribas", "JPMC", "Morgan Stanley", "Citi", "Goldman Sachs",
    "Bank of America", "Deutsche Bank", "UBS", "Barclays", "Credit Suisse",
    "Wells Fargo", "Nomura", "State Street", "BlackRock", "PIMCO",
    "Societe Generale", "Invesco", "AllianceBernstein", "MAN Group",
    "Charles Schwab", "Fidelity", "PineBridge", "Guggenheim", "Bain & Co",
    "Oracle", "SAP",

    # Quantitative Trading Firms, Hedge Funds, Prop Shops (including additions)
    "3Red Partners", "A Priori Investments", "Acadian Asset Management", "Akuna Capital",
    "Albatross Labs", "AlphaGrep", "AlphaSimplex", "Alphataraxia Management",
    "Alyeska Investment Group", "Ansatz Capital", "AQR Capital Management", "Aquatic Capital",
    "Arrowstreet Capital", "ART Advisors", "Aspect Capital", "AXQ Capital",
    "Balyasny Asset Management", "Banyan Alpha Investment", "Belvedere Trading",
    "BlackEdge Capital", "Bluefin Capital Management", "Blueshift Asset Management",
    "Boerboel Trading", "Boulder Hill Capital Management", "Brevan Howard",
    "Bridgewater Associates", "Cantor Fitzgerald", "Capital Fund Management",
    "Capital Markets Trading", "Capstone", "Capula Investment Management",
    "Caxton Associates", "Centiva Capital", "Chicago Trading Company", "Citadel",
    "Consolidated Trading", "CQS", "Cubist (part of Point72)", "Dark Forest",
    "DE Shaw", "Dolat Capital", "DRW", "Duality Group", "DV Trading",
    "Edgehog Trading", "Edgestream Partners", "Eisler Capital", "Elk Capital Markets",
    "Elequin Capital", "Emergent Trading", "Engineers Gate", "Ergoteles Capital",
    "Eschaton Trading", "Evergreen Statistical Trading", "ExodusPoint",
    "Five Rings", "Florin Court Capital", "Flow Traders", "Freestone Grove Partners",
    "G-Research", "GAM Systematic", "Garda Capital Partners", "Gelber Group",
    "Geneva Trading", "Geode Capital Management", "Graham Capital Management",
    "Graviton Research Capital", "Group One Trading", "GSA Capital Partners",
    "GTS", "HAP Capital", "Headlands Technologies", "Hudson Bay Capital",
    "Hudson River Trading", "IMC Financial Markets", "Jacobs Levy Equity Management",
    "Jain Global", "Jane Street", "Jocassee Quantitative", "Jump Trading",
    "Kepos Capital", "Kore Trading", "Kula Investments", "Laurion Capital Management",
    "Lord Abbett", "Lynx Asset Management", "Mako", "Man Group", "Mana Partners",
    "Marquette Partners", "Marshall Wace", "Maven Securities", "Millburn",
    "Monoceros", "Nebula Research & Development", "Old Mission Capital", "Optiver",
    "Paloma Partners", "PanAgora", "Parallax Volatility Advisers", "PDT Partners",
    "Peak6", "PGIM Quant Solutions", "Prime Trading", "QMS Capital Management",
    "Qsemble Capital Management", "Quadeye Securities", "Quadrature Capital",
    "Quantbot Technologies", "Quantbox Research", "Quantitative Investment Management",
    "Quantlab Financial", "Quantumrock Capital", "Qube Research & Technologies",
    "QVR Advisors", "Radix Trading", "Renaissance Technologies", "Rokos Capital Management",
    "Rosetta Analytics", "RSJ", "Schonfeld Strategic Advisors", "Segantii Capital Management",
    "Sensato Investors", "Seven Eight Capital", "Spark Investment Management",
    "Squarepoint Capital", "Stevens Capital Management", "Summit Securities Group",
    "Sumo", "Sunrise Futures", "Susquehanna International Group", "Systematica Investments",
    "Tanius Technology", "Teza Technologies", "TGS Management Company",
    "Tower Research Capital", "Tradebot", "Tradelink Holdings", "TransMarket Group",
    "Trexquant Investment", "Two Sigma", "Valkyrie Trading", "Vatic Investments",
    "Vector Trading", "Verition Fund Management", "Virtu Financial", "Volant Trading",
    "Voleon Group", "Voloridge Investment Management", "Volterra Technologies",
    "Walleye Capital", "WH Trading", "Wincent", "Winton Capital Management",
    "Wintermute", "Wolverine Trading", "WorldQuant", "Xantium (part of Tudor)",
    "XR Trading", "XTX Markets",

    # Additional known and top quant firms from recent rankings
    "QuantMatter", "FundedNext", "Estee Advisors", "Liquid Capital Group", "Mako",
    "Mandara", "Tibra", "TradeLink", "XY Capital", "Algorithmic Trading Group",
    "Eclipse Trading", "DV Trading", "Epoch", "Maven Securities", "Maverick Capital",
    "Five Rings Capital", "Susquehanna", "Tibra", "TradeLink", "VIRTU Financial",
    "WEBB Traders", "Wolverine Trading", "XR Trading", "XTX Markets", "XY Capital",

    # Major Technology Companies (High-paying for SDE/SWE roles)
    "Google", "Meta", "Microsoft", "Amazon", "Apple", "Netflix", "Adobe", "Salesforce", "ServiceNow",
    "Nvidia", "Intel", "Cisco", "Oracle", "SAP", "IBM", "Atlassian", "GitHub", "Twilio", "Palo Alto Networks",
    "Rubrik", "Asana", "Dropbox", "Zoom", "Stripe", "PayPal", "Visa", "American Express", "Walmart", "Uber",
    "Lyft", "Reddit", "Quora", "Pinterest", "LinkedIn", "GitLab", "Snowflake", "Coinbase", "Robinhood",
    "Square (Block)", "Shopify", "DoorDash", "Tesla", "Zscaler", "Palantir", "MongoDB", "Databricks",
    "ServiceNow", "Cloudflare", "Workday", "Slack", "HashiCorp", "Bloomberg", "Media.net", "CRED", "Razorpay",
    "Paytm", "Ola", "Dream11", "BrowserStack", "Flipkart", "Myntra", "Swiggy", "Zomato", "Zepto", "Meesho",
    "InMobi", "Lenskart", "Juspay", "Groww", "CoinSwitch", "PhonePe", "Zoho", "Freshworks", "Zeta",
    "BYJU'S", "Unacademy", "Delhivery", "Acko", "Udaan", "BigBasket", "Nykaa", "CureFit", "BlackRock",
    "JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Deutsche Bank", "American Express", "Bain & Company",
    "ServiceNow", "Lowes", "Intuit", "BD (Becton Dickinson)", "Awas", "Awfis", "Atlan", "Samsun", "Nvidia",
    "Qualcomm", "GitHub", "Github", "Linekdin", "LinkedIn", "DE Shaw", "Rubrik", "Tower Research",
    "BlackRock", "BCG", "Bain & Company", "McKinsey & Company", "Boston Consulting Group", "Oliver Wyman",
    "Roland Berger", "A.T. Kearney", "Accenture", "Deloitte", "PwC", "EY", "KPMG"
]

def connect_people(company_name):
    global driver
    print(f"\n🔍 Searching and connecting for: {company_name}")
    # Step 1: Search for the company
    try:
        search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
    except:
        try:
            search_box = driver.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input")
        except:
            print("❌ Search bar not found. LinkedIn may have updated its UI.")
            return
    
    search_box.clear()
    search_box.send_keys(company_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

        # Step 2: See all people
        try:
            see_all_people = driver.find_element(By.XPATH, "//a[contains(text(), 'See all people results')]")
            driver.execute_script("arguments[0].click();", see_all_people)
            time.sleep(5)
        except Exception:
            print("⚠️ Could not find 'See all people results'. Skipping company.")
            return

        # Step 3: Connect loop
        connections_sent = 0
        target_connections = 1

        while connections_sent < target_connections:
            connect_buttons = driver.find_elements(By.XPATH, "//button[span[text()='Connect']]")
            print(f"Found {len(connect_buttons)} connect buttons.")

            for button in connect_buttons:
                if connections_sent >= target_connections:
                    break
                try:
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)

                    send_without_note = driver.find_element(By.XPATH, "//button[span[text()='Send without a note']]")
                    driver.execute_script("arguments[0].click();", send_without_note)
                    time.sleep(2)

                    connections_sent += 1
                    print(f"✅ Sent connection request #{connections_sent}")

                except Exception as e:
                    print(f"⚠️ Error sending connect: {e}")
                    time.sleep(2)

            # Go to next page if needed
            if connections_sent < target_connections:
                try:
                    next_button = driver.find_element(By.XPATH, "//button[span[text()='Next']]")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(5)
                except Exception:
                    print("⚠️ No next button found. Ending.")
                    break

        print(f"✅ Finished connecting to {connections_sent} people for {company_name}.")

    except Exception as e:
        print(f"❌ Error during company '{company_name}': {e}")

try:
    # Step 0: LinkedIn login
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    # Randomly select a company
    random_company = random.choice(companies)
    connect_people(random_company)

finally:
    print("\n🚀 Done. Closing browser.")
    driver.quit()
