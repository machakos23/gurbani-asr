from flask import Flask, render_template, request
import time, tempfile, os
import preprocess, zmq

app = Flask(__name__)

@app.route('/')
def serve():
    return render_template('demo.html')

@app.route('/upload',methods=['POST'])
def process():
    file = request.files['audio']
    socket = zmq.Context().socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    
    with tempfile.NamedTemporaryFile() as tmp1, tempfile.NamedTemporaryFile(suffix='.flac') as tmp2:
        file.save(tmp1)
        try: 
            preprocess.preprocess(tmp1.name, vol=-3, cutoffdb=-25, minsilence=0.25, padding=0.15, fileoutpath=tmp2.name)
        except Exception as e: return "Error: <bad audio data>"

        socket.send_string(tmp2.name)
        result = socket.recv_string()
        socket.close()
        
        return result
    

@app.route('/test')
def test():
    return "ok"








