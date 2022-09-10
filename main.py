from flask import Flask, render_template, url_for, request, redirect, Response
from db import db_init, db
from werkzeug.utils import secure_filename
from models import Image
from decoder import convert_pic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///image.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)





@app.route('/')
def page_index():
    return render_template('index.html')

@app.route('/upload_img')
def page_upload_img():
    return render_template('upload_img.html')

@app.route('/upload', methods=['POST'])
def page_upload():
    pic = request.files['pic']
    pic_read = pic.read()
    if not pic:
        return 'No pic uploaded', 400
    decode, lang = convert_pic(pic_read)
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Image(img=pic_read, name=filename, mimetype=mimetype, language=lang, decode=decode)
    db.session.add(img)
    db.session.commit()

    return redirect('/')

@app.route('/<int:id>')
def get_img(id):
    img = Image.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)


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
