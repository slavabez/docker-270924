from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Docker!'

@app.route('/health')
def health():
    return 'OK'

@app.route('/version')
def version():
    return '1.0'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
