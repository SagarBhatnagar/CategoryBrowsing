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
    def __init__(self, Query, category, first, second, dispute, final):
        self.Query = Query
        self.category = category
        self.first = first
        self.second = second
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
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug = True)