from flask import Flask, Response, render_template, request
import requests
import hashlib
import redis

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "AMoAd"
default_name = 'Inseo Kim'


@app.route('/', methods=['GET', 'POST'])
def mainpage():
	selected_name = default_name
	if request.method == 'POST':
		selected_name = request.form['name']

	salted_name = salt + selected_name
	name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

	return render_template('index.html', name=selected_name, hash=name_hash)


@app.route('/monster/<name>')
def get_identicon(name):
	image = cache.get(name)
	if image is None:
		print ("Cache miss", flush=True)
		req = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
		image = req.content
		cache.set(name, image)

	return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
