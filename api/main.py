from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from sqlalchemy import func

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://foo:bar@mysql_database:3306/delphi'
app.config['JSON_SORT_KEYS'] = False


class Cheese(db.Model):
    __tablename__ = 'CHEESE_SCORES'

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    company = db.Column(db.String(128), nullable=False)
    product_name = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(256), nullable=False)
    county = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{self.product_name}: {self.rating}'


@app.route('/')
def home():
    return {
               'message': 'This is the main endpoint to the cheese rating API.'
           }, 200


@app.route('/cheese/')
def get_cheese():
    """
    :return: return all the cheeses that are present in database
    """
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


@app.route('/cheese/<int:id>', methods=['GET'])
def get_cheese_info(id: int):
    """
    :param id: cheese id
    :return: return the cheese of a given ID
    """
    cheese = Cheese.query.filter(Cheese.id == id).first_or_404()
    return jsonify(
        {
            'id': cheese.id,
            'company': cheese.company,
            'product_name': cheese.product_name,
            'rating': cheese.rating,
            'category': cheese.category,
            'county': cheese.county,
            'country': cheese.country
        }
    )


@app.route('/cheese/<country>', methods=['GET'])
def get_cheese_list_by_country(country: str):
    """
    :param country: country name (not case sensitive)
    :return: return all the cheeses within a given country
    """
    cheese_list = Cheese.query.filter_by(country=country).all()

    return jsonify([
        {
            'id': cheese.id,
            'company': cheese.company,
            'product_name': cheese.product_name,
            'rating': cheese.rating,
            'category': cheese.category,
            'county': cheese.county,
            'country': cheese.country
        } for cheese in cheese_list
    ])


@app.route('/cheese/countries', methods=['GET'])
def get_countries():
    """
    :return: return a unique list of all countries available in the database
    """
    return jsonify({
        'countries': [country[0] for country in db.session.query(Cheese.country.distinct()).all()]
    })


@app.route('/cheese/country_scores', methods=['GET'])
def get_country_scores():
    """
    :return: return the number of gold, bronze, silver and super gold awarded cheeses per country
    """
    country_scores = db.session.query(
        Cheese.country,
        Cheese.rating,
        func.count('*').label('rating_count')
    ).group_by(
        Cheese.country,
        Cheese.rating
    ).all()

    country_awards = {}

    for r in country_scores:
        if country_awards.get(r.country) is None:
            country_awards[r.country] = {}
        country_awards[r.country].update(
            {f"{'_'.join([w for w in r.rating.lower().split(' ')]) + '_awards'}": r.rating_count}
        )

    return jsonify([{'country': k, **v} for k, v in country_awards.items()])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
