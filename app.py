from flask import Flask, render_template, request, jsonify
import main

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('newhome.html')

@app.route('/video',methods=['GET',"POST"])
def video():
    if request.method == 'POST':
        data = request.form
        url = data['url']
        print(url)
        response = main.main(url=url)
        return jsonify({'status':True, 'response':response})
    return render_template('video.html')

# @app.post('/transcript')
# def transcript():
#     try:
#         data = request.form
#         url = data['url']
#         response = main.get_video_transcript(url) 
#         print(response)
#         return jsonify({'status':True, 'response':response})
#     except Exception as e:
#         print(str(e))
#         return jsonify({'status':False, 'response':"This video has no related captions"})

@app.post('/search/<string:search>')
def search(search):
    try:
        data = request.form 
        print(data)
        url = data['url']
        print(search)
        print(url)
        result = main.get_time_stamp(url=url, search=search)
        List = ['some content', 'shit']
        return jsonify({'status':True, 'list':List})
    except Exception as e:
        return jsonify({'status':False, 'message':f"Error:{e}"})

if __name__ == "__main__":
    app.run(debug=True)
