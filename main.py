from flask import Flask, render_template, request, redirect, Response
from db import db_init, db
from werkzeug.utils import secure_filename
from models import Image
from decoder import convert_pic
from datetime import datetime
import base64
import humanize

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///image.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route('/')
def page_index():
    _t = humanize.i18n.activate("ru_RU")
    db_image = Image.query.order_by(db.desc(Image.date)).all()
    now = datetime.utcnow()
    for el in db_image:
        el.img = base64.b64encode(el.img).decode('ascii')
        el.date = humanize.naturaltime(now - el.date)
    return render_template('index.html', db_image=db_image)


@app.route('/upload_img')
def page_upload_img():
    return render_template('upload_img.html')


@app.route('/upload', methods=['POST'])
def page_upload():
    pic = request.files['pic']
    pic_read = pic.read()
    if not pic:
        return 'Нет картинки'
    decode, lang = convert_pic(pic_read)
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Не удалось загрузить!'

    img = Image(img=pic_read, name=filename, mimetype=mimetype, language=lang, decode=decode)
    try:
        db.session.add(img)
        db.session.commit()
    except:
        return 'При загрузке в базу данных произошла ошибка!'
    return redirect('/')


@app.route('/id/<int:id>')
def get_img(id):
    img = Image.query.filter_by(id=id).first()
    if not img:
        return 'Картинка не найдена!'

    return Response(img.img, mimetype=img.mimetype)


@app.route('/id/<int:id>/del')
def del_img(id):
    img = Image.query.get_or_404(id)
    if not img:
        return 'Картинка не найдена!'
    try:
        db.session.delete(img)
        db.session.commit()

    except:
        return 'При удалении катинки произошла ошибка!'
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
