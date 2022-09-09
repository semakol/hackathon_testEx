from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     intro = db.Column(db.String(300), nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/create-article', methods=['POST', 'GET'])
# def create_article():
#     if request.method == 'POST':
#         title = request.form['title']
#         intro = request.form['intro']
#         article = Article(title=title, intro = intro)
#
#         try:
#             db.session.add(article)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'При добавлении статьи произошла ошибка'
#     else:
#         return render_template('create-article.html')
#
# @app.route('/posts')
# def posts():
#     articles = Article.query.order_by(Article.date).all()
#     return render_template('posts.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)
