from flask import Flask, request
import os


class Scheduler:
    @staticmethod
    def schedule(files):
        for file in files:
            Scheduler.__save_file(file)

    @staticmethod
    def __save_file(file):
        file.save(f"/usr/src/app/backend/static/{file.filename}")


app = Flask(import_name=__name__, static_url_path="/backend/static")


@app.route('/backend/health')
def health():
    return ''


@app.route("/backend/files", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("files[]")
    Scheduler.schedule(uploaded_files)
    return ""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
