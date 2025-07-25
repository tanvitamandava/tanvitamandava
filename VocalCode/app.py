from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import subprocess
import os
import sys
import json
import speech_recognition as sr
import requests
from threading import Event

app = Flask(__name__)
socketio = SocketIO(app)

# Directories for temporary user code storage
PYTHON_CODE_DIR = 'tmp/python_code'
CPP_CODE_DIR = 'tmp/cpp_code'
os.makedirs(PYTHON_CODE_DIR, exist_ok=True)
os.makedirs(CPP_CODE_DIR, exist_ok=True)

# Flags and events for control
current_prompt = ""
stop_flag = False
stop_typing_flag = False
response_event = Event()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/python')
def python_compiler():
    global current_prompt
    current_prompt = "Give Python file only nothing else , no explanations along with code ."
    return render_template('python.html')

@app.route('/cpp')
def cpp_compiler():
    global current_prompt
    current_prompt = "Give C++ file only nothing else , no explanations along with code  ."
    return render_template('cpp.html')

@app.route('/website')
def website_compiler():
    global current_prompt
    current_prompt = "Use only HTML , css , js . All HTML , CSS , JS should be in same code file .Don't give any explainations . Just make website for "
    return render_template('website.html')

# Route to run Python code
@app.route('/run_python', methods=['POST'])
def run_python_code():
    data = request.get_json()
    code = data.get('code', '')
    inputs = data.get('inputs', '')

    file_path = os.path.join(PYTHON_CODE_DIR, 'user_code.py')
    with open(file_path, 'w') as file:
        file.write(code)

    result = {'output': ''}
    try:
        completed_process = subprocess.run(
            [sys.executable, file_path],
            input=inputs,
            text=True,
            capture_output=True,
            timeout=5
        )
        result['output'] = completed_process.stdout + completed_process.stderr
    except subprocess.TimeoutExpired:
        result['output'] = 'Error: Code execution timed out.'
    except Exception as e:
        result['output'] = f'Error: {str(e)}'

    return jsonify(result)

# Route to run C++ code
@app.route('/run_cpp', methods=['POST'])
def run_cpp_code():
    data = request.get_json()
    code = data.get('code', '')
    inputs = data.get('inputs', '')

    cpp_file_path = os.path.join(CPP_CODE_DIR, 'user_code.cpp')
    executable_path = os.path.join(CPP_CODE_DIR, 'user_code.exe')
    
    with open(cpp_file_path, 'w') as file:
        file.write(code)

    result = {'output': ''}
    try:
        compile_process = subprocess.run(
            ['g++', cpp_file_path, '-o', executable_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if compile_process.returncode != 0:
            result['output'] = 'Compilation Error:\n' + compile_process.stderr
        else:
            run_process = subprocess.run(
                [executable_path],
                input=inputs,
                text=True,
                capture_output=True,
                timeout=5
            )
            result['output'] = run_process.stdout + run_process.stderr
    except subprocess.TimeoutExpired:
        result['output'] = 'Error: Code execution timed out.'
    except Exception as e:
        result['output'] = f'Error: {str(e)}'

    return jsonify(result)

def get_ollama_response(input_text):
    url = "http://localhost:11434/api/generate"
    data = {"model": "llama3.1", "prompt": input_text, "stream": True}
    try:
        # Use a session for better connection management
        with requests.Session() as session:
            response = session.post(url, json=data, stream=True)
            if response.status_code == 200:
                return response
            else:
                return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

def process_ollama_stream(response, socket):
    global stop_typing_flag, response_event
    
    try:
        for line in response.iter_lines():
            if stop_typing_flag:
                # Close the response connection
                response.close()
                break
                
            if line:
                try:
                    decoded_line = json.loads(line.decode('utf-8'))
                    socket.emit('output', {'message': decoded_line['response']})
                    
                    # If this is the last response from Ollama
                    if decoded_line.get('done', False):
                        break
                        
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"Error processing line: {e}")
                    continue
    finally:
        response_event.set()
        socket.emit('stop_streaming')

# Function to recognize speech and return text
def recognize_speech(audio):
    recognizer = sr.Recognizer()
    try:
        # Recognize the speech from the audio
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def callback(text):
    global stop_flag, current_prompt, stop_typing_flag, response_event
    
    socketio.emit('output', {'message': f"Your query: {text}"})
    stop_flag = True
    
    if text and text != "Sorry, I could not understand the audio.":
        stop_typing_flag = False
        response_event.clear()
        
        full_input = f" {text} {current_prompt}"
        response = get_ollama_response(full_input)
        
        if response:
            process_ollama_stream(response, socketio)
        else:
            socketio.emit('output', {'message': 'Failed to get response from Ollama'})
            socketio.emit('stop_streaming')
    
    response_event.set()

@socketio.on('stop_typing')
def stop_typing():
    global stop_typing_flag, response_event
    stop_typing_flag = True
    # Wait for the response processing to complete
    response_event.wait(timeout=2.0)
    socketio.emit('output', {'message': 'Response stopped by user'})
    socketio.emit('stop_streaming')

@socketio.on('start')
def start_recognition(text=None):
    global stop_typing_flag
    stop_typing_flag = False  # Reset the flag when starting new recognition
    start_streaming(text)

def start_streaming(text):
    global stop_flag
    if not text:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
        
        socketio.emit('start_streaming')

        stop_flag = False

        def listen_callback(recognizer, audio):
            stop_listening(wait_for_stop=False)
            text = recognize_speech(audio)
            callback(text)

        stop_listening = recognizer.listen_in_background(mic, listen_callback)
        try:
            while not stop_flag:
                pass
        finally:
            socketio.emit('stop_streaming')
            stop_listening(wait_for_stop=False)
            stop_flag = False
    else:
        socketio.emit('stop_streaming')

@socketio.on('manual_input')
def handle_manual_input(data):
    global stop_typing_flag
    text = data.get('text', '')
    if text:
        stop_typing_flag = False  # Reset the flag for new manual input
        callback(text)


@socketio.on('chat_message')
def handle_chat_message(data):
    text = data.get('text', '')
    if text:
        response = get_ollama_response(text)
        if response:
            for line in response.iter_lines():
                if line:
                    try:
                        decoded_line = json.loads(line.decode('utf-8'))
                        response_text = decoded_line.get('response', '')
                        
                        # Emit each part of the response in real-time
                        socketio.emit('chat_response', {
                            'message': response_text, 
                            'done': decoded_line.get('done', False)
                        })
                        
                        if decoded_line.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
        else:
            socketio.emit('chat_response', {
                'message': 'Failed to get a response from Ollama', 
                'done': True
            })

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
