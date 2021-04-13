import yaml
import re

from app import app
from flask import render_template, request
from generate import Generate


@app.route('/ui', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        return scan(request)
    return render_template('index.html')


def scan(request):
    hostname = request.form.get('host')
    username = request.form.get('username')
    password = request.form.get('password')
    protocol = request.form.get('igp')
    pattern = "(\d+\.){3}\d+"

    if re.search(pattern, hostname) == None:
        message = "Invalid IP address for host. Error '{}'".format(hostname)
        return render_template('index.html', message=message)

    config = {'hostname': hostname, 'username': username,
              'password': password, 'igp': protocol}

    with open('app/config.yaml', mode='w') as file:
        yaml.dump(config, file)

    generate_topology = Generate()
    generate_topology.start()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)