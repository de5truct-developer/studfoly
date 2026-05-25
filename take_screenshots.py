import sys, os, time
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--force-device-scale-factor=1')
options.add_argument('--lang=ru')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

base = 'https://studenthubs.duckdns.org'
screenshots_dir = r'C:\Users\s1mple\Desktop\проектнеый\screenshots'

# Find actual profile link from home page
print('Finding profile links from home page...')
driver.get(base + '/')
time.sleep(3)

# Find profile links
links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/accounts/profile/"]')
for link in links:
    href = link.get_attribute('href')
    if href and '/accounts/profile/' in href:
        print(f'  Found profile link: {href}')
        driver.get(href)
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshots_dir, 'profile.png'))
        print('  Saved profile screenshot')
        break

# Admin panel
print('Taking admin screenshot...')
driver.get(base + '/admin/')
time.sleep(3)
driver.save_screenshot(os.path.join(screenshots_dir, 'admin.png'))
print('  Saved admin')

driver.quit()
print('Done!')
