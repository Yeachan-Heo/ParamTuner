from flask import Flask
from flask import Blueprint, request, render_template, flash, redirect, url_for
from paramtuner import VariableHolder
from threading import Thread
VERSION="0.0.0"


class ParamTuner(VariableHolder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = Flask(__name__)
        self.app_thread = Thread(target=lambda: self.app.run(host="127.0.0.1", port=5000))
        self.main = self.app.route('/', methods=['GET'])(self.main)
        self.tune = self.app.route("/tune", methods=["POST"])(self.tune)
        self.exception = self.app.route("/exception", methods=["GET"])(self.exception)
        self.e = None

    def main(self):
        return render_template('/main/index.html', vh=self, version=VERSION)

    def exception(self):
        return render_template('/main/exception.html', exception=self.e)

    def tune(self):
        for key, value in request.form.items():
            if not value == '':
                try:
                    self.set_value(key, value)
                except Exception as e:
                    self.e = str(e)
                    return redirect(url_for("exception"))
        return redirect(url_for("main"))
        
    def items(self):
        return zip(self.varnames, map(self.get_value, self.varnames))

if __name__ == '__main__':
    pt = ParamTuner(a=1, b=2, c=3, d=4, e=343)
    pt.app_thread.start()