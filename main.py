from flask import Flask, render_template
import options

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

app.run(debug = options.debug_mode)