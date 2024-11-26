from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/scan', methods=['GET'])
def scan():
    student_name = request.args.get('student_name')
    
    try:
        with open("qr_states.json", "r") as file:
            qr_state = json.load(file)
    except FileNotFoundError:
        return "Error: qr_states.json file not found.", 500
    except json.JSONDecodeError:
        return "Error: qr_states.json contains invalid JSON.", 500
    
    if student_name in qr_state:
        if qr_state[student_name] == "unused":
            qr_state[student_name] = "used"
            with open("qr_states.json", "w") as file:
                json.dump(qr_state, file)
            return jsonify({"message": f"QR code for {student_name} is valid and now marked as used."})
        else:
            return jsonify({"message": f"QR code for {student_name} has already been used."})
    else:
        return jsonify({"message": f"QR code for {student_name} not found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
