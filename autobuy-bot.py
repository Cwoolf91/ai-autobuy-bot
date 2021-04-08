# MIT License

# Copyright (c) 2021 Chris Woolf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
from plyer import notification
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint, randrange

# Using my local profile that has saved passwords, etc.
localOptions = webdriver.ChromeOptions()
localOptions.add_argument(
    "user-data-dir=C:\\Users\\piano\\AppData\\Local\\Google\\Chrome\\User Data")

# Local path of the .exe chromedriver
browser = webdriver.Chrome(
    "/Documents/Development/ai-autobuy-bot/chromedriver", options=localOptions)

# 3080 RTX graphics card from Best Buy site.
browser.get("https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440")

### Following commented blocks were used for testing purposes with an in stock item. ###

# browser.get("https://bestbuy.com")

#input("Press enter to continue..")

# browser.get("https://www.bestbuy.com/site/amd-ryzen-9-3900x-3rd-generation-12-core-24-thread-3-8-ghz-4-6-ghz-max-boost-socket-am4-unlocked-desktop-processor/6356274.p?skuId=6356274")


# Following loop will randomly refresh the page and try to select the add to cart button.
buyButton = False

randomInterval = randint(1, 4)

while not buyButton:

    try:
        addToCartBtn = browser.find_element_by_css_selector(
            ".btn.btn-disabled.add-to-cart-button")
        print("Button is not ready yet.")
        time.sleep(randomInterval)
        browser.refresh()
        randomInterval = randint(1, 4)
    except:
        addToCartBtn = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".btn-primary.add-to-cart-button")))

        addToCartBtn.click()

        print("Button was clicked.")

        buyButton = True
        notification.notify(
            title="Add to cart button was clicked!",
            message="The item was added to the cart!",
            timeout=50
        )

goToCartBtn = WebDriverWait(browser, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".go-to-cart-button")))
goToCartBtn.click()

print("Go to cart button was clicked.")

shipToSelection = WebDriverWait(browser, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=fulfillment-shipping]")))
shipToSelection.click()
print("Shipping button selected.")

# checkoutButton = WebDriverWait(browser, 5).until(
#    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[2]/#div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button")))

checkoutButton = WebDriverWait(browser, 5).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "checkout-buttons__checkout")))
print("Checkout button clicked.")
checkoutButton.click()

# Sometimes a popup modal would happen and this block takes care of it.
# I then switched to using my Chrome profile with extensions to block popups, kept this in.
try:
    prequalOfferBtn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "prequal-offer-modal__btn")))
    print("Skip prequal offer button clicked.")
    prequalOfferBtn.click()

except:
    print("Prequal offer not found")

# This block is used when a popup to reenter credentials happens.
try:
    signInBtn = browser.find_element_by_xpath(
        "//*[contains(text(), 'Sign in with Google')]")
    print("Sign in button clicked.")
    notification.notify(
        title="Sign in page reached!",
        message="You need to sign in with google!",
        timeout=50
    )
    window_before = browser.window_handles[0]
    time.sleep(2)
    print("Sign in button clicked.")
    signInBtn.click()
    time.sleep(2)
    window_after = browser.window_handles[1]
    browser.switch_to_window(window_after)
    myEmail = browser.find_element_by_xpath(
        "//*[contains(text(), 'sampleemail@gmail.com')]")
    myEmail.click()
    time.sleep(5)
    browser.switch_to_window(window_before)
    time.sleep(5)
except:
    print("Cannot sign in")

# Enters in the CVV code... hardcoded
cvvSlot = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.ID, "credit-card-cvv")))
print("CVV entered")
cvvSlot.send_keys("XXX")

# Selects the send text notifications box
textUpdates = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.ID, "text-updates")))
print("Selecting send text updates.")
textUpdates.click()

# Select the purchase button
makePurchase = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, ".btn.btn-lg.btn-block.btn-primary.button__fast-track")))
print("Make purchase button clicked")
makePurchase.click()

# Sends desktop notifications
notification.notify(
    title="Purchase successful!",
    message="We win!",
    timeout=50
)
