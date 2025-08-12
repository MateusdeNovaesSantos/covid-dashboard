from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Um endpoint simples para verificar se a API está no ar.
    """
    return jsonify({"status": "healthy", "message": "Backend is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)