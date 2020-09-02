from flask import Flask,render_template,url_for,request,redirect,flash,jsonify


app = Flask(__name__)


@app.route('/', methods = ['POST', 'GET'])
@app.route('/1st/', methods = ['POST', 'GET'])
def fst():
	if request.method == 'POST':
		name = request.form['username1']
		movie = request.form['movie']
		seats = request.form['seats']

		return render_template("s2.html",name = name,movie = movie,seats=seats)




if __name__=='__main__':
	app.secret_key='nikhil'
	app.run(debug='true')