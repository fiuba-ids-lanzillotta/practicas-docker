from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Flask App')

@app.route('/info')
def info():
    return {
        'message': 'Esta es una API simple',
        'status': 'running',
        'version': '1.0'
    }

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5505)
