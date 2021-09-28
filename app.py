from flask import Flask,render_template,url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
import logging as logger

logger.basicConfig(level="DEBUG")
from click import command, echo
import os
from datetime import datetime
from flask.cli import with_appcontext
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app=Flask(__name__,template_folder='template')
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db=SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created =db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' %self.id
@app.route('/',methods=['POST','GET'])
def index():
    logger.debug("Post Call")
    if(request.method=='POST'):
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error was adding issue'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


if __name__== "__main__":
    logger.debug("Starting Flask Server")

    app.run(debug=True)