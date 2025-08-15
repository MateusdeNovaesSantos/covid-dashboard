from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CovidCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    cases = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'cases': self.cases,
            'deaths': self.deaths,
            'report_date': self.report_date.isoformat()
        }

