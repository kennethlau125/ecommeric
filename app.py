from flask import Flask,request,render_template,flash,redirect,url_for,session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

UPLOAD_FOLDER = 'HW/static/img/'

ALLOWED_EXTENSIONS = {}

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'basketball'

app.config["UPLOADED_IMAGES_DEST"]  = UPLOAD_FOLDER



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    isSuperUser = db.Column(db.Boolean(), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(120), unique=False, nullable=False)

class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clothesname = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(120), unique=False)


class Shoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shoesname = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(120), unique=False, nullable=False)

@app.route('/register', methods=["POST","GET"])
def register():

    if request.method == "POST":
        username = request.values.get('register_username')
        email = request.values.get('register_email')
        password = request.values.get('register_password')
        confirmPassword = request.values.get('register_confirm_password')
    
        had_user = User.query.filter_by(username = username).first()
        had_email = User.query.filter_by(email = email).first()

        if had_user:
            flash("used username")
        else:
            if had_email:
                flash("used email")
            else:
                if password == confirmPassword:
                    new_user = User(username=username,email=email,password=confirmPassword,isSuperUser=False)
                    db.session.add(new_user)
                    db.session.commit()
                else:
                    flash(" wrong password")


    return render_template('login.html')

@app.route('/',methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.values.get("login_username")
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == request.values.get('login_password'):
                session["userInFo"] = {user.id: {"name": user.username}}
                print(session)
                return redirect(url_for("home"))
                
            else:
                flash("Wrong Input")
                print(session)
                return redirect(url_for("login"))
        else:
            flash("Wrong Username Input")
            print(session)
            return redirect(url_for("login"))


    return render_template("login.html")



@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/clothes', methods=["POST","GET"])
def clothes():
        clothes = Clothes.query.all()
        return render_template('clothes.html',clothes=clothes)

@app.route('/shoes', methods=["POST","GET"])
def shoes():
    shoeses = Shoes.query.all()
    print(shoeses)
    return render_template('shoes.html',shoeses=shoeses)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/addclothes', methods=["POST","GET"])
def addclothes():
    if request.method == 'POST':
        product_name = request.values.get("clothes_name")
        image = request.values.get("clothes_image")
        price = request.values.get("clothes_price")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/img/',filename))

            new_clothes = Clothes(clothesname=product_name,image=filename,price=price)
            db.session.add(new_clothes)
            db.session.commit()
            
            return redirect(url_for('addclothes'))



    return render_template('addclothes.html')

@app.route('/addshoes', methods=["POST","GET"])
def addshoes():
    if request.method == 'POST':
        product_name = request.values.get("shoes_name")
        image = request.values.get("shoes_image")
        price = request.values.get("shoes_price")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/img/',filename))

            new_shoes = Shoes(shoesname=product_name,image=filename,price=price)
            db.session.add(new_shoes)
            db.session.commit()
            
            return redirect(url_for('addshoes'))



    return render_template('addshoes.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
  


