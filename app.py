from flask import Flask, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.secret_key = 'SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    d_o_b = db.Column(db.DateTime(), index=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Info('{self.name}', '{self.d_o_b}', '{self.email}', '{self.city})"

cities = [
    ('Cambridge', 'Cambridge'),
    ('London', 'London')
    ]

class DataForm(FlaskForm):
    name_input = StringField(label='Enter Your Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    email_address = StringField(label='Email Address', validators=[DataRequired(), Email()])
    city_input = SelectField('City', choices=cities)
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = DataForm()
    if form.validate_on_submit():
        data = Info(name=form.name_input.data, d_o_b=form.date_of_birth.data, email=form.email_address.data, city=form.city_input.data) 
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('output'))
    return render_template('home.html', form=form)

@app.route('/output')
def output():

    details = Info.query.order_by(Info.id.desc()).first()

    name_details = details.name
    dob_details = details.d_o_b
    email_details = details.email
    city_details = details.city




    return render_template('output.html', name=name_details, dob=dob_details, email=email_details, city=city_details)





if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)