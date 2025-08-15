import os
from flask import Flask, jsonify, request # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

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

@app.route("/api/countries", methods=["GET"])
def get_countries():
    """ Retorna uma lista única de todos os países no banco. """
    try:
        countries_query = db.session.query(CovidCase.country).distinct().order_by(CovidCase.country).all()
        country_list = [country[0] for country in countries_query]
        
        return jsonify(country_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route("/api/data", methods=["GET"])
def get_all_data():
    """ 
    Busca os dados de forma paginada e permite filtrar por país e data.
    Parâmetros:
    - page: O número da página (padrão: 1)
    - per_page: Itens por página (padrão: 20)
    - country: O nome do país para filtrar
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        country_filter = request.args.get('country', None, type=str)
        
        query = CovidCase.query
        
        if country_filter:
            query = query.filter(CovidCase.country.like(f"%{country_filter}%"))
            
        query = query.order_by(CovidCase.report_date.desc())
        paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)
        
        results = [case.to_dict() for case in paginated_data.items]
        
        return jsonify({
            "data": results,
            "pagination": {
                "page": paginated_data.page,
                "per_page": paginated_data.per_page,
                "total_pages": paginated_data.pages,
                "total_items": paginated_data.total,
                "has_next": paginated_data.has_next,
                "has_prev": paginated_data.has_prev
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)