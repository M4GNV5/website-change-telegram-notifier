#!/usr/bin/python3

import json
import base64
import hashlib
import telegram
import imgkit

with open("config.json", "r") as fd:
	config = json.load(fd)
with open("websites.json", "r") as fd:
	websites = json.load(fd)

bot = telegram.Bot(config["telegram-token"])
changed = False

for site in websites:
	try:
		content = imgkit.from_url(site["url"], False)
	except:
		continue

	digest = hashlib.sha512(content).digest()
	digest = base64.b64encode(digest).decode("ascii")

	if site["hash"] != digest:
		site["hash"] = digest
		changed = True

		msg = "{} changed!\n{}".format(site["name"], site["url"])
		bot.send_message(config["telegram-chat"], msg)

if changed:
	with open("websites.json", "w") as fd:
		json.dump(websites, fd, indent=4)
