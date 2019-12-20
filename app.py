from flask import Flask, render_template, url_for, redirect
from forms import LoginForm
import random
import json
import datetime
import secrets
import CameraController as cc

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(24)

camera = cc.CameraController()


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('app.html', title='Camera Controller', status=camera.getStatus())



if __name__ == '__main__':
    app.run(port=2609, debug=True, host="0.0.0.0")
