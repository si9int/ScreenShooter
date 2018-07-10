#!/usr/bin/env python
# m2p.py (v.0.2) - Screenshot your masscan-results via chromedriver in python
# written by SI9INT (twitter.com/si9int) | si9int.sh

import os, json, argparse, socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

from requests.packages.urllib3.exceptions import NewConnectionError

# Enter the path to your chromedriver and screenshot-directory
DVR_PATH = '/usr/bin/chromedriver'
PIC_PATH = './screens/'

parser = argparse.ArgumentParser()

parser.add_argument('file', help = 'masscan result', type = str)
parser.add_argument('-s', '--subdomain', help = 'result of a subdomain-scan', action = 'store_true')

args = parser.parse_args()

def initDriver():
	options = Options()

	# disable-dev-shm-usage: Debian-bugfix

	arguments = [
		'--headless',
		'--log-level=3',
		'--allow-insecure-localhost',
		'--disable-dev-shm-usage',
		'--no-sandbox',
		'--disable-extensions',
		'--disable-gpu',
		'--ignore-certificate-errors'
	]

	for argument in arguments:
		options.add_argument(argument)
	
	capabilities = DesiredCapabilities.CHROME.copy()
	capabilities['acceptSslCerts'] = True
	capabilities['acceptInsecureCerts'] = True

	driver = webdriver.Chrome(DVR_PATH, chrome_options=options, desired_capabilities=capabilities)
	driver.set_page_load_timeout(12)

	return driver

basename = PIC_PATH + os.path.basename(args.file)
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

def readSubs(file):
	log = open(file).readlines()

	for line in log:
		# add your ports here if you want custom web-instances being scanned
		ports = [80, 443]
		methods = ['http://', 'https://']
		line = line.rstrip()

		for i,port in enumerate(ports):
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(2)
				result = s.connect_ex((line, port))
				
				if result == 0:
					print('[-] Online: ' + line + ':' + str(port))

					if port == 8080:
						tmp.append(methods[i] + line + ':8080')
					else:
						tmp.append(methods[i] + line)
				
				s.close()
			except:
				print('[!] Error on: ' + line)
				pass

def appendHTML(name, url):
	if not os.path.isfile(basename + '/index.html'):
		overview = open(basename + '/index.html', 'w')
		os.system('xdg-open ' + basename + '/index.html')
	else:
		overview = open(basename + '/index.html', 'a')

	image = '<p><img src="' + str(name) + '.png"></p><hr>'
	link  = '<h2><a href="' + url + '" target="_blank">' + url + '</a></h2>'

	global htm
	overview.write(link + image)

def makeScreen(name, url, driver):
	try:
		driver.get(url)
		screenshot = driver.save_screenshot(basename + '/' + str(name) + '.png')
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

if not os.path.isdir(basename):
	os.makedirs(basename)

if args.subdomain:
	readSubs(args.file)
else:
	readLog(args.file)

for number,url in enumerate(tmp):
	if not makeScreen(number, url, driver):
		driver.close()
		driver = initDriver()
		print('[!] Driver restarted')

driver.quit()

print('[-] Overview created: ' + basename + '/index.html')
print('[!] Failed URLS:\n--')

for error in err:
	print('\t' + error)
