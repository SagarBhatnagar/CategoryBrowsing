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

class ItemTable(Table):
    Query = Col('Query')
    category = Col('Category')
    batch = Col('Batch')
    first = Col('Associate 1')
    second = Col('Associate 2')
    anno_first = Col('Annotation 1')
    anno_second = Col('Annotation 2')
    dispute = Col('Dispute')
    name = Col('Judgement By')
    final = Col('Final')

class Item(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    Query=db.Column(db.String(100))
    category=db.Column(db.String(100))
    batch=db.Column(db.String(100))
    first=db.Column(db.String(100))
    second=db.Column(db.String(100))
    anno_first=db.Column(db.String(100))
    anno_second=db.Column(db.String(100))
    dispute=db.Column(db.String(10))
    name=db.Column(db.String(100))
    final=db.Column(db.String(100))    
    def __init__(self, Query, category, batch, first, second, anno_first, anno_second, dispute, name, final):
        self.Query = Query
        self.category = category
        self.batch = batch
        self.first = first
        self.second = second
        self.anno_first = anno_first
        self.anno_second = anno_second
        self.dispute = dispute
        self.name = name
        self.final = final
app.secret_key = "super secret key"
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        Query = request.form.get('Query')
        category = request.form.get('category')
        batch = request.form.get('batch')
        first = request.form.get('first')
        second = request.form.get('second')
        anno_first = request.form.get('anno_first')
        anno_second = request.form.get('anno_second')
        name = request.form.get('name')
        final = request.form.get('final')

        query = Item.query
        if Query:
            query=query.filter(Item.Query == Query)
        if category:
            query=query.filter(Item.category == category)
        result=query.all()
        if result == []:
            dispute = "YES"
            if anno_first and anno_second:
                if anno_first == anno_second:
                    dispute = "NO"                
            item = Item(Query, category, batch, first, second, anno_first, anno_second, dispute, name, final)
            db.session.add(item)
            db.session.commit()
            flash('Added')
        else:
            result = result[0]
            flag = 0
            if result.final:
                flash('Already Judged')
                flag = 1
            else:
                result.final = final
            if first and not flag:
                result.first = first
            if second and not flag:
                result.second = second
            if anno_first and not flag:
                result.anno_first = anno_first
            if anno_second and not flag:
                result.anno_second = anno_second
            if result.anno_first and result.anno_second and not flag:
                if result.anno_first == result.anno_second:
                    result.dispute = "NO"
                    db.session.commit()
                else:
                    result.dispute = "YES"
                    db.session.commit()
            if name and not flag:
                result.name = name
            
            if not flag:
                flash('Added')
            db.session.commit()  
        
    return render_template('home.html')

@app.route('/search', methods = ["GET", "POST"])
def search():
    if request.method == "POST":
        Query = request.form.get('Query')
        category = request.form.get('category')
        dispute = request.form.get('dispute')
        batch = request.form.get('batch')
        query = Item.query
        if Query:
            query = query.filter(Item.Query == Query)
        if category:
            query = query.filter(Item.category == category)
        if dispute:
            query = query.filter(Item.dispute == dispute)
        if batch:
            query = query.filter(Item.batch == batch)    
        result = query.all()
        table = ItemTable(result)
        return render_template('search_results.html', table=table)
    return render_template('search.html')
if __name__ == '__main__':
    app.run(debug = True)