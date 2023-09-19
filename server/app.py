#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200


@app.route('/articles')
def index_articles():

    pass


@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    if request.method == 'GET':
        if 'page_views' not in session:
            session['page_views'] = 0
        elif session['page_views'] <= 3:
            article = Article.query.get(id)  # Retrieve the article by ID

            if article:
                session['page_views'] += 1
                article_dict = article.to_dict()
                response = make_response(jsonify(article_dict), 200)
            else:
                response = make_response(
                    jsonify({'error': 'Article not found'}), 404)
        else:
            response = make_response(
                jsonify({'message': 'Maximum pageview limit reached'}), 401)

    return response


if __name__ == '__main__':
    app.run(port=5555)
