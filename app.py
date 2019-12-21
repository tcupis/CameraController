import json

from flask import Flask, redirect, render_template, request, url_for

import CameraController as cc

app = Flask(__name__)

camera = cc.CameraController()


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if request.form['takePhoto'] and camera.getStatus():
            camera.takePhoto()

    return render_template('app.html', title='Camera Controller', status=camera.getStatus())



if __name__ == '__main__':
    app.run(port=2609, debug=True, host="0.0.0.0")
