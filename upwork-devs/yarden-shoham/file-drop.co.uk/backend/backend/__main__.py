from flask import Flask, request
app = Flask(__name__)


@app.route('/backend/health')
def health():
    return ''


@app.route("/backend/files", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("files[]")
    print(uploaded_files)
    return ""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
