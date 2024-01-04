from flask import Flask, render_template, request, jsonify
import main

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("newhome.html")


@app.route("/video", methods=["GET", "POST"])
def video():
    if request.method == "POST":
        data = request.form
        url = data["url"]

        response = main.main(url=url)
        # response = ({'transcript':"formatted_transcript", 'summary':"main_summary", 'quiz':"quiz"})
        return jsonify({"status": True, "response": response})
    return render_template("video.html")


@app.post("/search/<string:search>")
def search(search:str):
    try:
        data = request.form
        # print(data)
        url = data["url"]
        # print(search)
        # print(url)
        result = main.get_time_stamp(url=url, search=search)
        # List = ['some content', 'shit']
        return jsonify({"status": True, "Content": result})
    except Exception as e:
        return jsonify({"status": False, "message": f"Error:{e}"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
