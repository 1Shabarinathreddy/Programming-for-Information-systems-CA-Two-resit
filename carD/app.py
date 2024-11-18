from flask import Flask, render_template

app = Flask(__name__)
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'dynamic postgres db name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



@app.route('/')
def home():
    return render_template('index.html', message="Welcome to Flask!")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
