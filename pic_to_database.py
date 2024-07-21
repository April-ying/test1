# 這是把圖片存進資料庫的程式 改下面image_path去存就可以
# sql檔案是搭配load_pic
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, LargeBinary
from PIL import Image
import io

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://april0909:c7CslksYkeusqcvAkMecoFDQPIFuiPKp@dpg-cqcj0sg8fa8c73crb3u0-a.oregon-postgres.render.com/data_uire"

db = SQLAlchemy(app)

class ImageModel(db.Model):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    image_data = Column(LargeBinary)

def save_image_to_db(image_path):
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_byte_arr = img_byte_arr.getvalue()

    new_image = ImageModel(image_data=img_byte_arr)
    db.session.add(new_image)
    db.session.commit()
    print("Image saved to database successfully.")

if __name__ == "__main__":
    image_path = "static/colorblind_image/20.png"#目前存到20
    with app.app_context():
        db.create_all()  # 创建表
        save_image_to_db(image_path)
