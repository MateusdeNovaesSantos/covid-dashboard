import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO DE DADOS ---
# Define como a tabela de dados da covid será estruturada
class CovidCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    cases = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        """Converte o objeto para um dicionário, útil para o JSON."""
        return {
            'id': self.id,
            'country': self.country,
            'cases': self.cases,
            'deaths': self.deaths,
            'report_date': self.report_date.isoformat()
        }
        
# --- ROTAS DA API ---
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route("/api/data", methods=["GET"])
def get_all_data():
    """Busca todos os registros de casos de covid no banco."""
    try:
        with app.app_context():
            db.create_all()
        
        if not CovidCase.query.first():
            from datetime import date
            test_case = CovidCase(country="Brasil (Teste)", cases=100, deaths=5, report_date=date.today())
            db.session.add(test_case)
            db.session.commit()
        
        cases = CovidCase.query.order_by(CovidCase.report_date.desc()).all()
        results = [case.to_dict() for case in cases]
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)