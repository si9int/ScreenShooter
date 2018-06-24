#!/usr/bin/env python
# m2p.py (v.0.1) - Screenshot your masscan-results via chromedriver in python
# written by SI9INT (twitter.com/si9int) | si9int.sh

import os, json, argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

# Enter the path to your chromedriver and screenshot-directory
DVR_PATH = '/usr/bin/chromedriver'
PIC_PATH = './screens/'

parser = argparse.ArgumentParser()

parser.add_argument('file', help = 'masscan result', type = str)
args = parser.parse_args()

def initDriver():
	options = Options()

	# You can remove/edit optional arguments here
	# disable-dev-shm-usage: Debian-bugfix

	arguments = [
		'--headless',
		'--log-level=3',
		'--allow-insecure-localhost',
		'--disable-dev-shm-usage',
		'--no-sandbox',
		'--disable-extensions',
		'--disable-gpu'
	]

	for argument in arguments:
		options.add_argument(argument)

	driver = webdriver.Chrome(DVR_PATH, chrome_options=options)
	driver.set_page_load_timeout(12)

	return driver

driver = initDriver()
tmp = []
err = []
htm = ''

def readLog(file):
	log = open(file).readlines()
	for line in log:
		try:
			data = json.loads(line[:-2])

			if data['ports'][0]['port'] == 80 or data['ports'][0]['port'] == 8080:
				method = 'http://'
			else:
				method = 'https://'

			if data['ip'] not in tmp:
				tmp.append(method + data['ip'])
		except:
			print('[!] Error reading log-entry')
			pass

def appendHTML(name, url):
	overview = open(PIC_PATH + 'index.html', 'a')

	image = '<p><img src="' + str(name) + '.png"></p>'
	link  = '<h2><a href="' + url + '" target="_blank">' + url + '</a></h2>'

	global htm
	overview.write(link + image)

def makeScreen(name, url, driver):
	try:
		driver.get(url)
		screenshot = driver.save_screenshot(PIC_PATH + str(name) + '.png')
		appendHTML(name, url)
	
		print('[-] Screenshooted: ' + url)
		return True
	except UnexpectedAlertPresentException as e:
		print('[!] Error: ' + str(e))
		err.append(url)
		return False
	except TimeoutException as t:
		print('[!] Timeout: ' + str(t))
		err.append(url)
		return False

if not os.path.isdir(PIC_PATH):
	os.makedirs(PIC_PATH)

readLog(args.file)

for number,url in enumerate(tmp):
	
	if not makeScreen(number, url, driver):
		driver.close()
		driver = initDriver()
		print('[!] Driver restarted')

driver.quit()

print('[-] Overview created: ' + PIC_PATH + 'index.html')
print('[!] Failed URLS:\n--')

for error in err:
	print('\t' + error)

os.system('xdg-open ' + PIC_PATH + 'index.html')
