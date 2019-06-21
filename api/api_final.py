import flask
from flask import request, jsonify
import sqlite3
import url_utils
import collections 
import operator
import os
from django import db

#db.connections.close_all()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Change the Username according to your laptop
user_name = "aquarius31"
#This path is only for Linux Version, we can later extend it to Windows also
path = "/home/"+user_name+"/.config/google-chrome/Default/History"

#@app.route('/', methods=['GET'])
def stats():
	connection = sqlite3.connect(path, timeout=5)
	c = connection.cursor()
	query = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
	#c.execute("title from urls")
	c.execute(query)
	results = c.fetchall()
	c.close()
	return results

@app.route('/', methods=['GET'])
def counter():
	sites_count = {}
	results = stats()
	for url, count in results:
		url = url_utils.parse(url)
		if url in sites_count:
			sites_count[url] += 1
		else:
			sites_count[url] = 1

	sites_count_sorted = collections.OrderedDict(sorted(sites_count.items(), key=lambda kv: kv[1], reverse=True))
	#sites_count_sorted = sorted(sites_count)
	return jsonify(sites_count_sorted)

app.run()