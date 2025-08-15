from flask import jsonify, request
from sqlalchemy import func, desc
from . import api_bp
from ..models import db, CovidCase

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@api_bp.route("/countries", methods=["GET"])
def get_countries():
    """ Retorna uma lista única de todos os países no banco. """
    try:
        countries_query = db.session.query(CovidCase.country).distinct().order_by(CovidCase.country).all()
        country_list = [country[0] for country in countries_query]
        
        return jsonify(country_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/data", methods=["GET"])
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

@api_bp.route("/summary/by-country", methods=["GET"])
def get_summary_by_country():
    """ 
    Retorna um resumo dos dados agregados por país.
    Calcula o número máximo de casos e mortes para cada país
    e retorna os 10 principais países ordenados pelo número de casos.
    """
    try:
        summary_query = db.session.query(
            CovidCase.country,
            func.max(CovidCase.cases).label('total_cases'),
            func.max(CovidCase.deaths).label('total_deaths')
        ).group_by(
            CovidCase.country
        ).order_by(
            desc('total_cases')
        ).limit(10).all()
        
        results = [
            {
                "country": country,
                "total_cases": total_cases,
                "total_deaths": total_deaths
            }
            for country, total_cases, total_deaths in summary_query
        ]
        
        return jsonify(results)
    
    except Exception as e: return jsonify({"error": str(e)}), 500

