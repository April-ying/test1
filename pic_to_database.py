from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, LargeBinary
from PIL import Image
import io

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://april0909:TevhMabtcGLrRlyn1rqrnfVcI5sVIKsH@dpg-cr1ljs5umphs73afhad0-a.oregon-postgres.render.com/data_0ol7"
db = SQLAlchemy(app)

# class ImageModel(db.Model):
#     __tablename__ = 'color_blind_question_pic'
#     id = Column(Integer, primary_key=True)
#     image_data = Column(LargeBinary)
#     answer = Column(Integer)

class ImageModel(db.Model):
    __tablename__ = 'color_blind_ans_pic'
    id = Column(Integer, primary_key=True)
    image_data = Column(LargeBinary)
    answer = Column(Integer)


def save_images_to_db(image_paths, answers):
    if len(image_paths) != len(answers):
        raise ValueError("圖片數量和答案數量不匹配")

    images = []
    
    for image_path, answer in zip(image_paths, answers):
        with Image.open(image_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_byte_arr = img_byte_arr.getvalue()

        # 創建一個新的 ImageModel 實例，並將其添加到列表中
        new_image = ImageModel(image_data=img_byte_arr, answer=answer)
        images.append(new_image)
    
    # 一次性將所有圖片批量插入到資料庫中
    db.session.bulk_save_objects(images)
    db.session.commit()
    print(f"{len(images)} images and answers saved to database successfully.")

if __name__ == "__main__":
    # image_paths = [
    #     "static/colorblind_image/1.png",
    #     "static/colorblind_image/2.png",
    #     "static/colorblind_image/3.png",
    #     "static/colorblind_image/4.png",
    #     "static/colorblind_image/5.png",
    #     "static/colorblind_image/6.png",
    #     "static/colorblind_image/7.png",
    #     "static/colorblind_image/8.png",
    #     "static/colorblind_image/9.png",
    #     "static/colorblind_image/10.png",
    #     "static/colorblind_image/11.png",
    #     "static/colorblind_image/12.png",
    #     "static/colorblind_image/13.png",
    #     "static/colorblind_image/14.png",
    #     "static/colorblind_image/15.png",
    #     "static/colorblind_image/16.png",
    #     "static/colorblind_image/17.png",
    #     "static/colorblind_image/22.png",
    #     "static/colorblind_image/23.png",
    #     "static/colorblind_image/24.png",
    #     "static/colorblind_image/25.png",
    #     "static/colorblind_image/26.png",
    #     "static/colorblind_image/27.png",
    #     "static/colorblind_image/30.png",
    #     "static/colorblind_image/31.png",
    #     "static/colorblind_image/32.png",
    #     "static/colorblind_image/33.png",
    #     "static/colorblind_image/34.png",
    #     "static/colorblind_image/35.png",
    #     "static/colorblind_image/36.png",
    #     "static/colorblind_image/37.png",
    #     "static/colorblind_image/38.png",
    # ]
    image_paths = [
        "ans/1ans.png",
        "ans/2ans.png",
        "ans/3ans.png",
        "ans/4ans.png",
        "ans/5ans.png",
        "ans/6ans.png",
        "ans/7ans.png",
        "ans/8ans.png",
        "ans/9ans.png",
        "ans/10ans.png",
        "ans/11ans.png",
        "ans/12ans.png",
        "ans/13ans.png",
        "ans/14ans.png",
        "ans/15ans.png",
        "ans/16ans.png",
        "ans/17ans.png",
        "ans/22ans.png",
        "ans/23ans.png",
        "ans/24ans.png",
        "ans/25ans.png",
        "ans/26ans.png",
        "ans/27ans.png",
        "ans/30ans.png",
        "ans/31ans.png",
        "ans/32ans.png",
        "ans/33ans.png",
        "ans/34ans.png",
        "ans/35ans.png",
        "ans/36ans.png",
        "ans/37ans.png",
        "ans/38ans.png",
    ]
    answers = [12,8,6,29,57,5,3,15,74,2,6,97,45,5,7,16,73,26,42,35,96,100,100,100,100,100,100,100,100,100,100,100 ]  # 對應的答案列表 #不是數字的填100

    with app.app_context():
        db.create_all()  # 創建表
        save_images_to_db(image_paths, answers)
