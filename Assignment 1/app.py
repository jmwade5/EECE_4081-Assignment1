from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy
 
database = "sqlite:///brokenlaptops.db"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database

db = SQLAlchemy(app)


@app.route('/')
def index():
    brokenlaptop = BrokenLaptop.query.all()
    return render_template("index.html",brokenlaptop=brokenlaptop)
    

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(brokenlaptop)
        db.session.commit()
    brokenlaptop = BrokenLaptop.query.all()
    return render_template("create.html",brokenlaptop=brokenlaptop)
        

    
@app.route('/delete/<laptop_id>')
def delete(laptop_id):
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    db.session.delete(brokenlaptop)
    db.session.commit()
    
     
    brokenlaptop = BrokenLaptop.query.all() 
    return render_template("delete.html", brokenlaptop = brokenlaptop)
    

    
@app.route('/update/<laptop_id>', methods=['GET','POST']) # add id 
def update(laptop_id):
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    if request.form:
        brokenlaptop.brand = request.form.get("brand")
        brokenlaptop.price = request.form.get("price")

        db.session.commit()
        return redirect('/', code = 302)
    
    return render_template("update.html", brokenlaptop = brokenlaptop)

class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    

if __name__ == '__main__':
    app.run(debug=True)


#1. sqlalchemy.orm.exc.UnmappedInstanceError. You could add in some error checking and add a warning that the entry does not exist and ask for a diffferent entry
#2. Yes, you could just have all the pages redirect to the read page as done in the update module
#3. Yes, we do this with flask when using the from app import db

