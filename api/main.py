from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://foo:bar@127.0.0.1/delphi'

class Cheese(db.Model):
    __tablename__ = 'CHEESE_SCORES'

    id           = db.Column(db.BigInteger, primary_key=True, index=True)
    company      = db.Column(db.String(128), nullable=False)
    product_name = db.Column(db.String(128), nullable=False)
    rating       = db.Column(db.String(128), nullable=False)
    category     = db.Column(db.String(256), nullable=False)
    county       = db.Column(db.String(128), nullable=False)
    country      = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{self.product_name}: {self.rating}'

@app.route('/')
def home():
    return {
        'message': 'This is the main endpoint to the cheese rating API.'
    }, 200

@app.route('/cheese/')
def get_cheese():
    return jsonify([
        {
            'id': cheese.id,
            'company': cheese.company,
            'product_name': cheese.product_name,
            'rating': cheese.rating,
            'category': cheese.category,
            'county': cheese.county,
            'country': cheese.country
        } for cheese in Cheese.query.all()
    ])

if __name__ == '__main__':
    app.run()