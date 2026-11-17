"""Browser tests for the palindrome checker page."""

import os
import threading
import time
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app import app


def _wait_until_ready(url: str, timeout: float = 15) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except URLError:
            time.sleep(0.2)
    raise RuntimeError(f"Application did not become ready at {url}")


@pytest.fixture(scope="module")
def base_url():
    configured = os.environ.get("PALINDROME_BASE_URL")
    if configured:
        _wait_until_ready(configured.rstrip("/") + "/health")
        yield configured.rstrip("/")
        return

    thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=7070, use_reloader=False),
        daemon=True,
    )
    thread.start()
    url = "http://127.0.0.1:7070"
    _wait_until_ready(url + "/health")
    yield url


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def check(browser, base_url, text):
    browser.get(base_url + "/")
    field = browser.find_element(By.ID, "text-input")
    field.clear()
    field.send_keys(text)
    browser.find_element(By.ID, "check-btn").click()
    result = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "result"))
    )
    return result


def test_palindrome_string(browser, base_url):
    result = check(browser, base_url, "A man a plan a canal Panama")
    assert result.get_attribute("data-palindrome") == "true"
    assert "is a palindrome" in result.text


def test_non_palindrome_string(browser, base_url):
    result = check(browser, base_url, "kubernetes")
    assert result.get_attribute("data-palindrome") == "false"
    assert "is not a palindrome" in result.text


def test_numeric_palindrome(browser, base_url):
    result = check(browser, base_url, "12321")
    assert result.get_attribute("data-palindrome") == "true"
    assert "12321" in result.text
