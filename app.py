from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
import datetime
import os

#App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initialize database
db = SQLAlchemy(app)

class Item(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    Query=db.Column(db.String(100))
    category=db.Column(db.String(100))
    first=db.Column(db.String(100))
    second=db.Column(db.String(100))
    anno_first=db.Column(db.String(100))
    anno_second=db.Column(db.String(100))
    dispute=db.Column(db.String(10))
    final=db.Column(db.String(100))    
    def __init__(self, Query, category, first, second, anno_first, anno_second, dispute, final):
        self.Query = Query
        self.category = category
        self.first = first
        self.second = second
        self.anno_first = anno_first
        self.anno_second = anno_second
        self.dispute = dispute
        self.final = final
app.secret_key = "super secret key"
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        Query = request.form.get('Query')
        category = request.form.get('category')
        first = request.form.get('first')
        second = request.form.get('second')
        anno_first = request.form.get('anno_first')
        anno_second = request.form.get('anno_second')
        query = Item.query
        if Query:
            query=query.filter(Item.Query == Query)
        if category:
            query=query.filter(Item.category == category)
        result=query.all()
        if result == []:
            if anno_first and anno_second:
                if anno_first == anno_second:
                    dispute = "NO"
                else:
                    dispute = "YES"
            item = Item(Query, category, first, second, anno_first, anno_second, dispute, " ")
            db.session.add(item)
            db.session.commit()
            flash('Added')
        else:
            result = result[0]
            if first:
                result.first = first
            if second:
                result.second = second
            if anno_first:
                result.anno_first = anno_first
            if anno_second:
                result.anno_second = anno_second
            if anno_first and anno_second:
                if anno_first == anno_second:
                    result.dispute = "NO"
                    db.session.commit()
                else:
                    result.dispute = "YES"
                    db.session.commit()
            db.session.commit()   
        
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug = True)