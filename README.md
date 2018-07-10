# ScreenShooter
Convert your masscan/subdomain-scan results (80,443,8080) into screenshots for better analysis .
**v.0.3 all issues have been fixed!**

**Installation**

```
pip3 install selenium
apt install chromium
# download latest version of chromedriver: http://chromedriver.chromium.org/downloads
# unpack to e.g. /usr/bin/
# configure your driver-path (DVR_PATH) and image-path (PIC_PATH) in m2p.py
```

**Usage**

```
usage: exe.py [-h] [-s] file

positional arguments:
  file             masscan result

optional arguments:
  -h, --help       show this help message and exit
  -s, --subdomain  result of a subdomain-scan

```
ScreenShooter will take a masscan-result by default. If you want to use a list of subdomains add `-s` as additional parameter.

**Example**

First we do a masscan (it's important to save the result in JSON)
`masscan 127.0.0.1/24 -p80,8080,443 -oJ output.json`
Than we execute exe.py with our log as argument:
`python3 exe.py output.json`

**Sampe result**

![1](https://user-images.githubusercontent.com/38978231/41800050-28d4c842-7674-11e8-8864-48b7ae617888.png)

Generated `index.html` for inspecting the result:

![2](https://user-images.githubusercontent.com/38978231/41800052-290bb4b0-7674-11e8-8aee-edc60fe829b2.png)
