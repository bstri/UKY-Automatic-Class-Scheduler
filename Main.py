import requests
import getpass
from lxml import html

URL = "https://myuk.uky.edu/irj/portal"
HIDDEN_NAMES = ["login_submit", "login_do_redirect", "no_cert_storing", "j_salt"]

session = requests.Session()
# Make the webpage think we're using Chrome
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

# populate hidden fields with current values
r = session.get(URL)
tree = html.fromstring(r.text)
hiddenDict = {}
for name in HIDDEN_NAMES:
	toFind = "//input[@name='{0}']/@value".format(name)
	hiddenDict[name] = tree.xpath(toFind)[0]

usr = input("Enter linkblue ID (myuk username): ")
pwd = getpass.getpass("Enter password: ")
r = session.post(URL, data = hiddenDict.update({"j_username": usr, "j_password": pwd}))
# username and password no longer needed
del pwd 
del usr
