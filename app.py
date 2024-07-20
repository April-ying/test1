# 統整版 用這個啟動
from flask import Flask, render_template,request, jsonify
from flask_socketio import SocketIO, send,emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import base64
from PIL import Image
from io import BytesIO
from sqlalchemy.sql.expression import func
import random

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://april0909:c7CslksYkeusqcvAkMecoFDQPIFuiPKp@dpg-cqcj0sg8fa8c73crb3u0-a.oregon-postgres.render.com/data_uire"

db = SQLAlchemy(app)
socketio = SocketIO(app)

    
#所有圖片
class pic(db.Model):
    __tablename__='cblind_spot_pic'#色盲點圖圖片
    id=db.Column(db.Integer,primary_key=True)
    addr=db.Column(db.String(150))

    def __init__(self,addr):
        self.addr=addr



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def start():
    return render_template('quiz.html')

@app.route('/qrcode')
def qrcode():
    return render_template('qrcode.html')

@app.route('/camera')
def choose():
    return render_template('camera_try.html')

@app.route('/myopia')
def confirm():
    return render_template('myopia.html')


@app.route('/generic')
def generic():
    random_id = random.randint(1, 10)
    colorblind_test=db.session.query(pic).filter(pic.id==random_id)
    for result in colorblind_test:
        print(result.addr)
    
    return render_template('handwrite.html',data=result.addr)

#切換下一題
@app.route('/next-image')
def next_image():
    random_id = random.randint(1, 10)
    colorblind_test = db.session.query(pic).filter(pic.id == random_id)
    for result in colorblind_test:
        print(result.addr)
    if colorblind_test:
        return jsonify({'nextImageUrl': result.addr})
    else:
        return jsonify({'error': 'No image found'}), 404

@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/contact')
def contact():
    return render_template('index1.html')

@app.route('/qrcodehandwrite')
def handwrite():
    return render_template('handwrite.html')

@app.route('/show')
def show():
    return render_template('show.html')

#確定是否以掃描QRcode進入色盲點圖測驗的頁面
@app.route('/color_blind_spot_map')
def color_blind_spot_map():
    return render_template('color_blind_spot_map.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json  # 從 POST 請求中獲取 JSON 格式的數據(前端傳來的圖片資料)
    # 檢查是否有圖片資料被傳遞過來
    if 'image' not in data:
        return jsonify({'error': 'No image data found'})
    
    image_data = data['image']  # 從 JSON 數據中提取名為 'image' 的 key 所對應的 value(前端傳來的圖片資料Base64格式字串)
    image_data = image_data.replace('data:image/png;base64,', '')  # 去除了 DataURL 的前綴部分
    # 將經過處理的 Base64 字符串解碼成二進制數據
    # 然後使用 BytesIO 將其包裝成 BytesIO 對象
    # 最後使用 Pillow 的 Image.open() 方法打開圖片，生成一個 Image
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image.save('uploaded_image.png')  # 將打開的圖片對象保存為 PNG 格式的圖片檔案
    # socketio.emit('image_uploaded', {'url': '/show'})
    return jsonify({'message': 'Image uploaded successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  #host改為0.0.0.0,讓手機暫時可以連上
    
