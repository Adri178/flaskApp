from flask import Flask, render_template, Response
from simulasi_bola import main_simulation_function  # Ganti dengan fungsi simulasi Anda

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    while True:
        frame = main_simulation_function()  # Panggil fungsi simulasi Anda di sini
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
