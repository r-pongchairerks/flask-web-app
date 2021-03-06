from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Il0veyou@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Il0veyou@localhost/lexus'    
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app )

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(f"{customer},{dealer},{rating},{comments}")
        
        if customer == "" or dealer == "":
            return render_template("index.html", message="Please enter required fields")
        
        my_customer = Feedback.query.filter_by(customer=customer).count()
        print(my_customer)
        if not my_customer:
            customer = Feedback(customer, dealer, rating, comments)
            db.session.add(customer)
            db.session.commit()
            
            # send mail
            send_mail(customer, dealer, rating, comments)
            
            return render_template("success.html")
        
    return render_template("index.html", message="You already submitted the feedback.")
          
        
    
    
if __name__ == "__main__":
    
    app.run()