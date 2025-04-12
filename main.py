# script by @szvy on github
# completely free to use
# https://github.com/szvy/fastly-automation
# luv yall <3

import requests
import time
import secrets
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import datetime
import os


def goonts(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]


nums = goonts("nums.txt")
chars = goonts("chars.txt")
simple = goonts("simple.txt")
skibidigyattoblock = goonts("skibidigyattoblock.txt")

print("\nchoose how your fastly links are generated:")
print("1. random numbers")
print("2. random characters")
print("3. english words")
print("4. brainrot")

genhowansnow = None
while genhowansnow not in ["1", "2", "3", "4"]:
    genhowansnow = input("enter a number (1-4): ")

if genhowansnow == "1":
    genhowans = nums
elif genhowansnow == "2":
    genhowans = chars
elif genhowansnow == "3":
    genhowans = simple
else:
    genhowans = skibidigyattoblock

moneyspread = random.sample(genhowans, 2)

if genhowansnow in ["3", "4"]:
    domainfromdagen = f"{moneyspread[0]}_{moneyspread[1]}"
else:
    domainfromdagen = f"{moneyspread[0]}{moneyspread[1]}"

os.makedirs("gen", exist_ok=True)

timee = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
exportfile = f"gen\\fastly {timee}.txt"

firstlink = f"https://{domainfromdagen}.global.ssl.fastly.net"

with open(exportfile, "a") as f:
    f.write(
        "links made with the fastly automation tool by https://github.com/szvy/fastly-automation"
        + "\n"
        + "\n"
    )
    f.write(firstlink + "\n")

goon = {
    "1": {"domain": "szvy.website", "site": "szvy central"},
    "2": {"domain": "truffled.lol", "site": "truffled"},
    "3": {"domain": "mexi.rest", "site": "meximath"},
    "4": {"domain": "frogiesarca.de", "site": "frogie's arcade"},
    "5": {"domain": "css.lat", "site": "css.lat"},
    "6": {"domain": "example.com", "site": "custom"},
}

print("\nselect a site to use with fastly:")
for num, details in goon.items():
    print(f"{num}. {details['site']}")

choice = None
while choice not in goon:
    choice = input("enter a number (1-6): ")

if choice == "6":
    custom_domain = input("enter a link (dont include https://): ")
    reversegoon = custom_domain
else:
    reversegoon = goon[choice]["domain"]

links = input("amount of links: ")
linksintvers = int(links) - 1


MAILTM_BASE = "https://api.mail.tm"


def create_mailtm_account():
    session = requests.Session()
    domains = session.get(f"{MAILTM_BASE}/domains").json()["hydra:member"]
    domain = domains[0]["domain"]
    username = "".join(
        secrets.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )
    email = f"{username}@{domain}"
    password = "".join(
        secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*")
        for _ in range(12)
    )

    session.post(
        f"{MAILTM_BASE}/accounts", json={"address": email, "password": password}
    )
    token_response = session.post(
        f"{MAILTM_BASE}/token", json={"address": email, "password": password}
    )
    token = token_response.json()["token"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    return email, password, session


def genpass(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    numbers = "".join(secrets.choice(string.digits) for _ in range(10))
    return password + numbers


email, mailtm_pass, mailtm_session = create_mailtm_account()
print(f"email: {email}")
password = genpass()
print(f"password: {password}")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://manage.fastly.com")

try:
    startbutton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Sign up']]"))
    )
    startbutton.click()

    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "FirstName"))
    ).send_keys("ScriptBy")
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "LastName"))
    ).send_keys("Szvy")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Company"))
    ).send_keys("szvydotwin")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Role"))
    ).send_keys("DevOps - Leadership")
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "Email"))
    ).send_keys(email)
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "Password"))
    ).send_keys(password)

    print("fastly is verifying your password (may take a moment)")
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Create a developer account']]")
        )
    ).click()

    print("account generated")

    try:
        captcha_present = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[contains(@src, 'captcha')]")
            )
        )
        if captcha_present:
            print("CAPTCHA DETECTED, PLEASE COMPLETE THE CAPTCHA")
            WebDriverWait(driver, 600).until_not(
                EC.presence_of_element_located(
                    (By.XPATH, "//iframe[contains(@src, 'captcha')]")
                )
            )
    except:
        pass

    print("waiting for verification email")
    verify = None
    for i in range(60):
        msgs = mailtm_session.get(f"{MAILTM_BASE}/messages").json()["hydra:member"]
        if msgs:
            print(f"verification email received")
            msg_id = msgs[0]["id"]
            msg_data = mailtm_session.get(f"{MAILTM_BASE}/messages/{msg_id}").json()
            html_content = msg_data["html"][0] if msg_data["html"] else ""
            soup = BeautifulSoup(html_content, "html.parser")
            a_tag = soup.find("a", href=True)
            if a_tag:
                verify = a_tag["href"]
                print(f"verifiying account")
                break
        time.sleep(5)

    if verify:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(verify)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    ).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continue']]"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    ).send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Log in']]"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Skip']]"))
    ).click()
    time.sleep(3)
    driver.get(driver.current_url.rsplit("/", 1)[0] + "/configure")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Create service']")
        )
    ).click()
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "serviceName"))
    )
    input_field.clear()
    input_field.send_keys("githubdotcomslashszvy")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "domain"))
    ).send_keys(domainfromdagen + ".global.ssl.fastly.net")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "host"))
    ).send_keys(reversegoon)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Activate']]"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Edit configuration')]")
        )
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Clone version 1 (active) to edit')]")
        )
    ).click()
    print("loading config edit")
    time.sleep(3)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Settings']"))
    ).click()
    driver.get(driver.current_url.rsplit("/", 1)[0] + "/settings/caches/new")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Name"))
    ).send_keys("sizzle")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "TTL"))
    ).send_keys("0")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "StaleTtl"))
    ).send_keys("0")
    cacheshit = Select(driver.find_element(By.NAME, "action"))
    cacheshit.select_by_visible_text("Pass")
    cacheshit.select_by_value("pass")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and normalize-space(text())='Create']")
        )
    ).click()
    # link creation loop
    driver.get(driver.current_url.replace("/settings", "/domains"))
    driver.get(driver.current_url.replace("/caches/new", "/"))
    for _ in range(linksintvers):
        if genhowansnow in ["3", "4"]:
            domainfromdagen = f"{random.choice(genhowans)}_{random.choice(genhowans)}"
        else:
            domainfromdagen = f"{random.choice(genhowans)}{random.choice(genhowans)}"

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Create domain')]")
            )
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "domain-name"))
        ).send_keys(domainfromdagen + ".global.ssl.fastly.net")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'primary') and contains(., 'Add')]",
                )
            )
        ).click()
        justmade = f"https://{domainfromdagen}.global.ssl.fastly.net"
        print("link created - " + justmade)
        with open(exportfile, "a") as f:
            f.write(justmade + "\n")
        time.sleep(0.2)
    # end of link creation loop
    print("all links have been made, saving")
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Activate')]"))
    ).click()
    driver.get(driver.current_url.replace("/versions/2/domains/", ""))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@title="Purge…"]'))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Purge all')]"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "service-name"))
    ).send_keys("githubdotcomslashszvy")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Purge all')]"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Okay')]"))
    ).click()

    exported = os.path.abspath(exportfile)
    time.sleep(2)
    driver.quit()
    os.startfile(exported)

finally:
    input(
        "thank you for using the fastly automation tool! your links have been exported to "
        + exported
    )
