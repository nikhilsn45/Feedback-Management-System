from flask import Flask,render_template,url_for,request,redirect,flash,jsonify
import mysql.connector
import xlrd, pdfcrowd
import pandas as pd
from pandas import ExcelFile
import random
import datetime
from datetime import date
from waitress import serve

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="nikhilsn123",
  database="feedbck",
  auth_plugin='mysql_native_password'
)

c = mydb.cursor(buffered=True)

c1 = 'create table IF NOT EXISTS `admin` (`username` varchar(15) not null unique,`post` varchar(25) not null,`college` varchar(70) not null,`dept` varchar(50) not null,`password` varchar(30) not null)'
c.execute(c1)
c2 = 'create table IF NOT EXISTS `faculty` (`college` varchar(70) not null,`dept` varchar(50) not null,`year` varchar(10) not null,`division` varchar(10) not null,`subject` varchar(50) not null,`subteacher` varchar(70) not null,`type` varchar(15) not null,`batch` varchar(10) not null)'
c.execute(c2)
c3 = 'create table IF NOT EXISTS `feedback3` (`college` varchar(70) not null,`dept` varchar(50) not null,`vishay` varchar(50) not null,`year1` varchar(10) not null,`div1` varchar(5) not null ,`teach` varchar(70) not null,`coo1` int,`pro1` int,`fas1` int,`low1` int,`improp` int,`pre` int,`syla` int,`dnot` int,`pun` int,`tecspeed` int,`msg` varchar(50),`date` varchar(25))'
c.execute(c3)
c4 = 'create table IF NOT EXISTS `pracfeed4` (`college` varchar(70) not null,`dept` varchar(50) not null,`vishay` varchar(50) not null,`year1` varchar(10) not null,`div1` varchar(5) not null ,`teach` varchar(70) not null,`msg` varchar(50) not null,`coo1` int,`pro1` int,`fas1` int,`low1` int,`improp` int,`pre` int,`date` varchar(25))'
c.execute(c4)
c.execute('create table IF NOT EXISTS `performance` (`college` varchar(70) not null,`dept` varchar(50) not null,`teach` varchar(70),`year1` varchar(5),`div1` varchar(5),`subject` varchar(50),`coo1` int,`pro1` int,`fas1` int,`low1` int,`improp` int,`pre` int,`syla` int,`dnot` int,`pun` int,`tecspeed` int,`totperform` int,`date` varchar(25))')
c.execute('create table IF NOT EXISTS `elecperformance` (`college` varchar(70) not null,`dept` varchar(50) not null,`teach` varchar(70),`year1` varchar(5),`subject` varchar(50),`coo1` int,`pro1` int,`fas1` int,`low1` int,`improp` int,`pre` int,`syla` int,`dnot` int,`pun` int,`tecspeed` int,`totperform` int,`date` varchar(25))')
c.execute('create table IF NOT EXISTS `pracperformance` (`college` varchar(70) not null,`dept` varchar(70) not null,`teach` varchar(70),`year1` varchar(5),`div1` varchar(5),`subject` varchar(50),`coo1` int,`pro1` int,`fas1` int,`low1` int,`improp` int,`pre` int,`totperform` int,`date` varchar(25))')

c.execute('create table IF NOT EXISTS `elective` (`college` varchar(70) not null,`dept` varchar(50) not null,`teach` varchar(70),`el1` varchar(50),`el2` varchar(50))')
c.execute('create table IF NOT EXISTS `stcount` (`college` varchar(70) not null,`dept` varchar(50) not null,`year` varchar(70),`div` varchar(50),`count` int)')
c.execute('create table IF NOT EXISTS `feedcount` (`college` varchar(70) not null,`dept` varchar(50) not null,`year` varchar(70),`div` varchar(50),`yes` varchar(10))')

app = Flask(__name__)



@app.route('/', methods = ['POST', 'GET'])
@app.route('/home/', methods = ['POST', 'GET'])
def home():
	if request.method == 'GET':
		c.execute('select distinct `college` from `admin`')
		res1 = c.fetchall()
		c.execute('select distinct `dept` from `admin`')
		res2 = c.fetchall()
		return render_template('index.html',res = res1,ress =res2)
	elif request.method == 'POST':
		c.execute('select distinct `college`,`dept` from `admin`')
		res1 = c.fetchall()
		return render_template('index.html',res = res1,ress =res2)


@app.route('/admin/', methods = ['POST', 'GET'])
def admin():
	if request.method == 'POST':
		return render_template('adminsiup.html')
	success = 'Successfully Done'
	return render_template('adminsiup.html' , success = success)


@app.route('/logout/', methods = ['POST', 'GET'])
def logout():
	return redirect(url_for('admin'))

@app.route('/home1/', methods = ['POST', 'GET'])
def home1():
	if request.method == 'POST':
		user = request.form['user']
		c.execute('select `college` , `dept` ,`username` from `admin` where `username` = %s',(user,))
		res1 = c.fetchall()
		return render_template('1111.html' , res = res1)


@app.route('/login/',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user = request.form['username1']
		passkey =request.form['pass']
		c.execute('select `password` from `admin` where `username` = %s',(user,))
		res1 = c.fetchone()
		if res1 != None:
			if res1[0] == passkey:
				c.execute('select `college` , `dept` ,`username` from `admin` where `username` = %s',(user,))
				res1 = c.fetchall()
				return render_template('1111.html' , res = res1)
			else:
				error ='incorrect username or password!!!!'
				return render_template('adminsiup.html' , error = error)
		error ='incorrect username or password!!!!'
		return render_template('adminsiup.html' , error = error)
	else:
		return render_template('1111.html')


@app.route('/signup/',methods = ['POST', 'GET'])
def signup():
	if request.method == 'POST':
		clg = request.form['clgnm']
		dept = request.form['deptnm']
		uname=request.form['uname']
		post=request.form['position']
		pas=request.form['pass1']
		common=request.form['common']
		c.execute('select `username` from `admin` where `username` = %s',(uname,))
		res = c.fetchone()
		if res != None:
			flash("Choose another user name!!!!")
			return render_template('adminsiup.html')

		c.execute('select `college`, `dept` from `admin` where `college` = %s and `dept` = %s',(clg,dept,))
		res = c.fetchone()
		if res != None:
			flash("Department Alredy exist for college")
			return render_template('adminsiup.html')

		if pas == common:
			c.execute('insert into `admin` (`username`,`post`,`college`,`dept`,`password`) values(%s,%s,%s,%s,%s)',(uname,post,clg,dept,pas,))
			mydb.commit()
			
			
			return redirect(url_for('admin'))
		return render_template('adminsiup.html')

@app.route('/feedback/',methods = ['POST', 'GET'])
def feedback():
	if request.method == 'POST':
		clg = request.form['clg']
		dept = request.form['dept']
		year = request.form['year']
		divi = request.form['division']
		batch = request.form['batch']

		if year == 'BE':
			el1 = request.form['el1']
			tea1 = request.form['tea1']
			el2 = request.form['el2']
			tea2 = request.form['tea2']


		c.execute("select `subject`, `subteacher` from `faculty` where `division` = %s and year = %s and college = %s and dept = %s and type = 'th'", (divi,year,clg,dept,))
		res = c.fetchall()
		c.execute("select `subject`, `subteacher` from `faculty` where `division` = %s and year = %s and college = %s and dept = %s and type = 'pr' and `batch` = %s", (divi,year,clg,dept,batch,))
		res1 = c.fetchall()

		
		if res == [] :
			c.execute('select distinct `college` from `admin`')
			res1 = c.fetchall()
			c.execute('select distinct `dept` from `admin`')
			res2 = c.fetchall()
			alt = 'nik'
			return render_template('index.html',alt = alt,res =res1,ress = res2)
		if res1 == [] :
			c.execute('select distinct `college` from `admin`')
			res1 = c.fetchall()
			c.execute('select distinct `dept` from `admin`')
			res2 = c.fetchall()
			alt = 'nik'
			return render_template('index.html',alt1 = alt,res =res1,ress = res2)

		n = random.randint(1,10000)
		tab = 'view' + str(n)
		c.execute("Create table IF NOT EXISTS `%s` As select `subject`, `subteacher` from `faculty` where `division` = %s and year = %s and college = %s and dept = %s and type = 'TH'",(tab,divi, year,clg,dept,))

		if year == 'BE':
			c.execute('insert into `%s` (subject,subteacher) values(%s,%s)',(tab,el1,tea1))
			mydb.commit()
			c.execute('insert into `%s` (subject,subteacher) values(%s,%s)',(tab,el2,tea2))
			mydb.commit()

		c.execute("select `subject`, `subteacher` from `%s`", (tab,))
		res45 = c.fetchall()


		return render_template('feedback.html',res = res45,year = year,div = divi,batch = batch,clg = clg,dept = dept,view=tab)


@app.route('/sendfeed/',methods = ['POST', 'GET'])
def sendfeed():
	if request.method == 'POST':
		d1 = request.form['teachersub']
		d2 = d1.split(' - ')
		sub = d2[0]
		teacher = d2[1]
		poor = request.form.get('poor')
		eng = request.form.get('eng')
		fas = request.form.get('fas')
		low = request.form.get('low')
		improp = request.form.get('improp')
		pre = request.form.get('pre')
		syla = request.form.get('syla')
		dnot = request.form.get('dnot')
		pun = request.form.get('pun')
		tecspeed = request.form.get('tecspeed')

		msg = request.form['msg']

		yea = request.form['y']
		divi = request.form['d']
		batch = request.form['b']
		clg = request.form['clg']
		dept = request.form['dept']
		nik = request.form['view']	

		today = date.today()
		d2 = today.strftime("%B %d, %Y")

		c.execute('insert into `feedback3` (`college`,`dept`,`vishay`,`year1`,`div1`,`teach`,`coo1`,`pro1`,`fas1`,`low1`,`improp`,`pre`,`syla`,`dnot`,`pun`,`tecspeed`,`msg`,`date`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(clg,dept,sub,yea,divi,teacher,poor,eng,fas,low,improp,pre,syla,dnot,pun,tecspeed,msg,d2))
		mydb.commit()

		c.execute('delete from `%s` where subject = %s and subteacher = %s',(nik,sub,teacher))
		mydb.commit()

		c.execute('select * from `%s`',(nik,))
		ttt = c.fetchall()

		if ttt == []:
			c.execute('drop table `%s`',(nik,))

			c.execute('select count(yes) from `feedcount` where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',(clg,dept,yea,divi,))
			r1 = c.fetchall()[0]
			print(r1)
			print(r1[0])
			if r1[0] == 0:
				ye = '1'
				c.execute('insert into `feedcount` (`college`,`dept`,`year`,`div`,`yes`) values(%s,%s,%s,%s,%s)',(clg,dept,yea,divi,ye,))
				mydb.commit()
			elif r1[0] > 0:
				c.execute('select * from `feedcount` where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',(clg,dept,yea,divi))
				r11 = c.fetchall()
				count = r11[0][4]
				count1 = int(count)
				yes = count1 + 1
				c.execute('update `feedcount` set `yes` = %s where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',(yes,clg,dept,yea,divi))
				mydb.commit()

			n = random.randint(1,10000)
			tab = 'view1' + str(n)
			c.execute("Create table IF NOT EXISTS `%s` As select `subject`, `subteacher` from `faculty` where `division` = %s and year = %s and college = %s and dept = %s and type = 'PR' and batch = %s",(tab,divi,yea,clg,dept,batch,))
			
			c.execute('select * from `%s`',(tab,))
			res = c.fetchall()
			return render_template('practicalfeed.html',res = res,year = yea,div = divi,batch = batch,clg = clg,dept = dept,view=tab)

		success = "Feedback submitted for " + teacher

		return render_template('feedback.html',res = ttt,year = yea,div = divi, batch = batch,success = success,clg = clg , dept = dept,view =nik)



@app.route('/sendpracfeed/',methods = ['POST', 'GET'])
def sendpracfeed():
	if request.method == 'POST':
		d1 = request.form['teachersub']
		d2 = d1.split(' - ')
		sub = d2[0]
		teacher = d2[1]

		poor = request.form.get('poor')
		eng = request.form.get('eng')
		fas = request.form.get('fas')
		low = request.form.get('low')
		improp = request.form.get('improp')
		pre = request.form.get('pre')
		msg = request.form['message']

		yea = request.form['y']
		di = request.form['d']
		clg = request.form['clg']
		dept = request.form['dept']
		batch = request.form['b']
		view = request.form['view']

		today = date.today()
		d2 = today.strftime("%B %d, %Y")

		c.execute('insert into `pracfeed4` (`college`,`dept`,`vishay`,`year1`,`div1`,`teach`,`msg`,`coo1`,`pro1`,`fas1`,`low1`,`improp`,`pre`,`date`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(clg,dept,sub,yea,di,teacher,msg,poor,eng,fas,low,improp,pre,d2,))
		mydb.commit()

		c.execute('delete from `%s` where subject = %s and subteacher = %s',(view,sub,teacher))
		mydb.commit()

		c.execute('select * from `%s`',(view,))
		ttt = c.fetchall()
		if ttt == []:
			c.execute('drop table `%s`',(view,))
			return redirect(url_for('home'))

		success = "Feedback submitted for " + teacher
		return render_template('practicalfeed.html',res = ttt,year = yea,div = di, batch = batch,success = success,clg = clg , dept = dept,view =view)


@app.route('/down/',methods = ['POST', 'GET'])
def down():
	if request.method=='POST':
		clg = request.form['clg']
		dept = request.form['dept']
		user = request.form['user']
		
		c.execute('select distinct `subteacher` from `faculty` where college = %s and dept = %s and `type` ="TH"',(clg,dept))
		re0 = c.fetchall()
		l = len(re0)
		for i in range(0,l):
			re00 = re0[i][0]
			c.execute('select distinct `year` from `faculty` where subteacher = %s and college = %s and dept = %s',(re00,clg,dept))
			re1 = c.fetchall()
			l1 = len(re1)
			for j in range(0,l1):
				re11 = re1[j][0]
				c.execute('select distinct `division` from `faculty` where subteacher = %s and year = %s and college = %s and dept = %s',(re00,re11,clg,dept))
				re2 = c.fetchall()
				l2 = len(re2)
				for k in range(0,l2):
					re22 = re2[k][0]
					c.execute('select distinct `subject` from `faculty` where subteacher = %s and year = %s and division = %s and college = %s and dept = %s',(re00,re11,re22,clg,dept))
					re3 = c.fetchall()
					l3 = len(re3)
					for m in range(0,l3):
						sum1=0
						sum2=0
						sum3=0
						sum4=0
						sum5=0
						sum6=0
						sum7=0
						sum8=0
						sum9=0
						sum10=0
						re33 = re3[m][0]
						teacher = re00
						year = re11
						div = re22
						sub = re33

						c.execute('select count(teach) from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',(div,year,teacher,sub,clg,dept,))
						total = c.fetchone()[0]
						if total != 0:

							c.execute('select `coo1` from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',(div,year,teacher,sub,clg,dept,))
							cnt1 = c.fetchall()
							for i in range(0,len(cnt1)):
								sum1 =sum1 + cnt1[i][0]
							sum11 = sum1/len(cnt1)

							c.execute('select pro1 from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt2 = c.fetchall()
							for i in range(0,len(cnt2)):
								sum2 =sum2 + cnt2[i][0]
							sum22 = sum2/len(cnt2)

							c.execute('select fas1 from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt3 = c.fetchall()
							for i in range(0,len(cnt3)):
								sum3 =sum3 + cnt3[i][0]
							sum33 = sum3/len(cnt3)

							c.execute('select low1 from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt4 = c.fetchall()
							for i in range(0,len(cnt4)):
								sum4 =sum4 + cnt4[i][0]
							sum44 = sum4/len(cnt4)

							c.execute('select improp from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt5 = c.fetchall()
							for i in range(0,len(cnt5)):
								sum5 =sum5 + cnt5[i][0]
							sum55 = sum5/len(cnt5)

							c.execute('select pre from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt6 = c.fetchall()
							for i in range(0,len(cnt6)):
								sum6 =sum6 + cnt6[i][0]
							sum66 = sum6/len(cnt6)

							c.execute('select syla from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt7 = c.fetchall()
							for i in range(0,len(cnt7)):
								sum7 =sum7 + cnt7[i][0]	
							sum77 = sum7/len(cnt7)

							c.execute('select dnot from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt8 = c.fetchall()
							for i in range(0,len(cnt8)):
								sum8 =sum8 + cnt8[i][0]	
							sum88 = sum8/len(cnt8)

							c.execute('select pun from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt9 = c.fetchall()
							for i in range(0,len(cnt9)):
								sum9 =sum9 + cnt9[i][0]	
							sum99 = sum9/len(cnt9)

							c.execute('select tecspeed from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt10 = c.fetchall()
							for i in range(0,len(cnt10)):
								sum10 =sum10 + cnt10[i][0]	
							sum100 = sum10/len(cnt10)

							

							sum0 = sum11+sum22+sum33+sum44+sum55+sum66+sum77+sum88+sum99+sum100
							totperf = sum0/10

							c.execute('select `date` from `feedback3` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							dat = c.fetchall()
							d2 = dat[0][0];

							c.execute('select count(teach) from `performance` where `teach` = %s and `year1` = %s and `div1` = %s and `subject` = %s and college = %s and dept = %s',(teacher,year,div,sub,clg,dept,))
							cntt = c.fetchone()[0]
							if cntt == 0:
								c.execute('insert into `performance` (`college`,`dept`,`teach`,`year1`,`div1`,`subject`,`coo1`,`pro1`,`fas1`,`low1`,`improp`,`pre`,`syla`,`dnot`,`pun`,`tecspeed`,`totperform`,`date`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(clg,dept,teacher,year,div,sub,sum11,sum22,sum33,sum44,sum55,sum66,sum77,sum88,sum99,sum100,totperf,d2))
								mydb.commit()
							else:
								c.execute('update `performance` set `coo1` = %s,`pro1` = %s,`fas1` = %s,`low1` = %s,`improp` = %s,`pre` = %s,`syla` = %s,`dnot` = %s,`pun` = %s,`tecspeed` = %s,`totperform` = %s where `teach` = %s and `year1` = %s and `div1` = %s and `subject` = %s  and college = %s and dept = %s' ,(sum11,sum22,sum33,sum44,sum55,sum66,sum77,sum88,sum99,sum100,totperf,teacher,year,div,sub,clg,dept,))


		c.execute('select distinct `teach` from `elective` where college = %s and dept = %s ',(clg,dept))
		re0 = c.fetchall()
		le0 = len(re0)

		c.execute('select distinct `el1` from `elective` where college = %s and dept = %s ',(clg,dept))
		re1 = c.fetchall()
		

		c.execute('select distinct `el2` from `elective` where college = %s and dept = %s ',(clg,dept))
		re2 = c.fetchall()
		le2 = len(re2)

		for a in range(0,le2):
			re1.append(re2[a])
		le1 = len(re1)

		for t in range(0,le0):
			for j in range(0,le1):
				teacher = re0[t][0]
				sub = re1[j][0]

				sum1=0
				sum2=0
				sum3=0
				sum4=0
				sum5=0
				sum6=0
				sum7=0
				sum8=0
				sum9=0
				sum10=0

				c.execute('select count(teach) from `feedback3` where `teach` = %s and `vishay` = %s and `college` = %s and `dept` = %s',(teacher,sub,clg,dept,))
				total = c.fetchone()[0]
				if total != 0:
					c.execute('select `coo1` from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',(teacher,sub,clg,dept,))
					cnt1 = c.fetchall()
					for i in range(0,len(cnt1)):
						sum1 =sum1 + cnt1[i][0]
					sum11 = sum1/len(cnt1)

					c.execute('select pro1 from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt2 = c.fetchall()
					for i in range(0,len(cnt2)):
						sum2 =sum2 + cnt2[i][0]
					sum22 = sum2/len(cnt2)

					c.execute('select fas1 from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt3 = c.fetchall()
					for i in range(0,len(cnt3)):
						sum3 =sum3 + cnt3[i][0]
					sum33 = sum3/len(cnt3)

					c.execute('select low1 from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt4 = c.fetchall()
					for i in range(0,len(cnt4)):
						sum4 =sum4 + cnt4[i][0]
					sum44 = sum4/len(cnt4)

					c.execute('select improp from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt5 = c.fetchall()
					for i in range(0,len(cnt5)):
						sum5 =sum5 + cnt5[i][0]
					sum55 = sum5/len(cnt5)

					c.execute('select pre from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt6 = c.fetchall()
					for i in range(0,len(cnt6)):
						sum6 =sum6 + cnt6[i][0]
					sum66 = sum6/len(cnt6)

					c.execute('select syla from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt7 = c.fetchall()
					for i in range(0,len(cnt7)):
						sum7 =sum7 + cnt7[i][0]	
					sum77 = sum7/len(cnt7)

					c.execute('select dnot from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt8 = c.fetchall()
					for i in range(0,len(cnt8)):
						sum8 =sum8 + cnt8[i][0]	
					sum88 = sum8/len(cnt8)

					c.execute('select pun from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt9 = c.fetchall()
					for i in range(0,len(cnt9)):
						sum9 =sum9 + cnt9[i][0]	
					sum99 = sum9/len(cnt9)

					c.execute('select tecspeed from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s  and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					cnt10 = c.fetchall()
					for i in range(0,len(cnt10)):
						sum10 =sum10 + cnt10[i][0]	
					sum100 = sum10/len(cnt10)


					sum0 = sum11+sum22+sum33+sum44+sum55+sum66+sum77+sum88+sum99+sum100
					totperf = sum0/10

					c.execute('select `date` from `feedback3` where `year1` = "BE" and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((teacher,sub,clg,dept,)))
					dat = c.fetchall()
					d2 = dat[0][0];

					c.execute('select count(teach) from `elecperformance` where `teach` = %s and `year1` = "BE" and `subject` = %s and college = %s and dept = %s',(teacher,sub,clg,dept,))
					cntt = c.fetchone()[0]
					if cntt == 0:
						year = "BE"
						c.execute('insert into `elecperformance` (`college`,`dept`,`teach`,`year1`,`subject`,`coo1`,`pro1`,`fas1`,`low1`,`improp`,`pre`,`syla`,`dnot`,`pun`,`tecspeed`,`totperform`,`date`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(clg,dept,teacher,year,sub,sum11,sum22,sum33,sum44,sum55,sum66,sum77,sum88,sum99,sum100,totperf,d2))
						mydb.commit()
					else:
						c.execute('update `elecperformance` set `coo1` = %s,`pro1` = %s,`fas1` = %s,`low1` = %s,`improp` = %s,`pre` = %s,`syla` = %s,`dnot` = %s,`pun` = %s,`tecspeed` = %s,`totperform` = %s where `teach` = %s and `year1` = %s and `subject` = %s  and college = %s and dept = %s' ,(sum11,sum22,sum33,sum44,sum55,sum66,sum77,sum88,sum99,sum100,totperf,teacher,year,sub,clg,dept,))


		c.execute('select distinct `subteacher` from `faculty` where college = %s and dept = %s and `type` = "PR"',(clg,dept))
		re0 = c.fetchall()
		l = len(re0)
		for i in range(0,l):
			re00 = re0[i][0]
			c.execute('select distinct `year` from `faculty` where subteacher = %s and college = %s and dept = %s',(re00,clg,dept))
			re1 = c.fetchall()
			l1 = len(re1)
			for j in range(0,l1):
				re11 = re1[j][0]
				c.execute('select distinct `division` from `faculty` where subteacher = %s and year = %s and college = %s and dept = %s',(re00,re11,clg,dept))
				re2 = c.fetchall()
				l2 = len(re2)
				for k in range(0,l2):
					re22 = re2[k][0]
					c.execute('select distinct `subject` from `faculty` where subteacher = %s and year = %s and division = %s and college = %s and dept = %s',(re00,re11,re22,clg,dept))
					re3 = c.fetchall()
					l3 = len(re3)
					for m in range(0,l3):
						sum1=0
						sum2=0
						sum3=0
						sum4=0
						sum5=0
						sum6=0
						sum7=0
						sum8=0
						sum9=0
						sum10=0
						re33 = re3[m][0]
						teacher = re00
						year = re11
						div = re22
						sub = re33

						c.execute('select count(year1) from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',(div,year,teacher,sub,clg,dept,))
						total = c.fetchone()[0]
						if total != 0:

							c.execute('select `coo1` from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',(div,year,teacher,sub,clg,dept,))
							cnt1 = c.fetchall()
							for i in range(0,len(cnt1)):
								sum1 =sum1 + cnt1[i][0]
							sum11 = sum1/len(cnt1)

							c.execute('select pro1 from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt2 = c.fetchall()
							for i in range(0,len(cnt2)):
								sum2 =sum2 + cnt2[i][0]
							sum22 = sum2/len(cnt2)

							c.execute('select fas1 from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt3 = c.fetchall()
							for i in range(0,len(cnt3)):
								sum3 =sum3 + cnt3[i][0]
							sum33 = sum3/len(cnt3)

							c.execute('select low1 from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt4 = c.fetchall()
							for i in range(0,len(cnt4)):
								sum4 =sum4 + cnt4[i][0]
							sum44 = sum4/len(cnt4)

							c.execute('select improp from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt5 = c.fetchall()
							for i in range(0,len(cnt5)):
								sum5 =sum5 + cnt5[i][0]
							sum55 = sum5/len(cnt5)

							c.execute('select pre from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							cnt6 = c.fetchall()
							for i in range(0,len(cnt6)):
								sum6 =sum6 + cnt6[i][0]
							sum66 = sum6/len(cnt6)

							sum0 = sum11+sum22+sum33+sum44+sum55+sum66
							totperf = sum0/6

							c.execute('select `date` from `pracfeed4` where `div1` = %s and `year1` = %s and `teach` = %s and `vishay` = %s and college = %s and dept = %s',((div,year,teacher,sub,clg,dept,)))
							dat = c.fetchall()
							d2 = dat[0][0];

							c.execute('select count(year1) from `pracperformance` where `teach` = %s and `year1` = %s and `div1` = %s and `subject` = %s and college = %s and dept = %s',(teacher,year,div,sub,clg,dept,))
							cntt = c.fetchone()[0]
							if cntt == 0:
								c.execute('insert into `pracperformance` (`college`,`dept`,`teach`,`year1`,`div1`,`subject`,`coo1`,`pro1`,`fas1`,`low1`,`improp`,`pre`,`totperform`,`date`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(clg,dept,teacher,year,div,sub,sum11,sum22,sum33,sum44,sum55,sum66,totperf,d2))
								mydb.commit()
							else:
								c.execute('update `pracperformance` set `coo1` = %s,`pro1` = %s,`fas1` = %s,`low1` = %s,`improp` = %s,`pre` = %s,`totperform` = %s where `teach` = %s and `year1` = %s and `div1` = %s and `subject` = %s  and college = %s and dept = %s' ,(sum11,sum22,sum33,sum44,sum55,sum66,totperf,teacher,year,div,sub,clg,dept,))


		c.execute('select * from `performance` where college = %s and dept = %s order by year1,div1,teach',(clg,dept))
		r = c.fetchall()
		c.execute('select * from `pracperformance` where college = %s and dept = %s order by year1,div1,teach',(clg,dept))
		r1 = c.fetchall()
		c.execute('select * from `elecperformance` where college = %s and dept = %s order by teach',(clg,dept))
		r2 = c.fetchall()
		c.execute('select * from `feedcount` where college = %s and dept = %s order by year',(clg,dept))
		r3 = c.fetchall()
		c.execute('select * from `stcount` where college = %s and dept = %s order by year',(clg,dept))
		r4 = c.fetchall()

		return render_template('perform1.html',resu = r,resu1 = r1,resu2 = r2,resu3 = r3,resu4 = r4,user = user)

@app.route('/exdn/',methods = ['POST', 'GET'])
def excel():
	user = request.form['user']
	return render_template("perform.html" , user = user)

@app.route('/pdf/',methods = ['POST', 'GET'])
def pdf():
	user = request.form['user']
	clg = request.form['clg']
	dept = request.form['dept']

	c.execute('select * from `performance` where college = %s and dept = %s order by teach',(clg,dept))
	r = c.fetchall()
	c.execute('select * from `pracperformance` where college = %s and dept = %s order by teach',(clg,dept))
	r1 = c.fetchall()
	
	co = []
	co1 = []
	co2 = []
	co3 = []

	l3 = len(r)
	for i in range(0,l3):
		year = r[i][3]
		divi = r[i][4]
		c.execute('select * from `stcount` where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',((clg,dept,year,divi,)))
		count = c.fetchone()
		if count == None:
			temp = 00
			co.append(temp)
		else:
			co.append(count[4])

	l3 = len(r)
	for i in range(0,l3):
		year = r[i][3]
		divi = r[i][4]
		c.execute('select * from `feedcount` where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',((clg,dept,year,divi,)))
		count = c.fetchone()
		if count == None:
			temp = 00
			co1.append(temp)
		else:
			co1.append(count[4])

	l3 = len(r1)
	for i in range(0,l3):
		year = r1[i][3]
		divi = r1[i][4]
		c.execute('select * from `stcount` where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',((clg,dept,year,divi,)))
		count = c.fetchone()
		if count == None:
			temp = 00
			co2.append(temp)
		else:
			co2.append(count[4])

	l3 = len(r1)
	for i in range(0,l3):
		year = r1[i][3]
		divi = r1[i][4]
		c.execute('select * from `feedcount` where `college` = %s and `dept` = %s and `year` = %s and `div` = %s ',((clg,dept,year,divi,)))
		count = c.fetchone()
		if count == None:
			temp = 00
			co3.append(temp)
		else:
			co3.append(count[4])


	d2 = r[0][14]

	x = []

	l3 = len(r)
	for i in range(0,l3):
		teach = r[i][2]
		year = r[i][3]
		divi = r[i][4]
		sub = r[i][5]
		y = []
		c.execute('select * from `feedback3` where college = %s and dept = %s and teach = %s and year1 = %s and div1 = %s and vishay = %s order by teach',(clg,dept,teach,year,divi,sub))
		tea = c.fetchall()
		le = len(tea)
		for j in range(0,le):
			if tea[j][13] != "":
				y.append(tea[j][13])

		x.append(y)

		a = []

	l3 = len(r1)
	for i in range(0,l3):
		teach = r1[i][2]
		year = r1[i][3]
		divi = r1[i][4]
		sub = r1[i][5]
		b = []
		c.execute('select * from `pracfeed4` where college = %s and dept = %s and teach = %s and year1 = %s and div1 = %s and vishay = %s order by teach',(clg,dept,teach,year,divi,sub))
		tea = c.fetchall()
		le = len(tea)
		for j in range(0,le):
			if tea[j][6] != "":
				b.append(tea[j][6])

		a.append(b)

	today = datetime.date.today()
	today_year = str(today.year)

	if today.month >= 6:
		nex = str(today.year + 1)
		cyea = today_year + "-" + nex
		sem = "SEM-1"
	else:
		nex = str(today.year - 1)
		cyea = nex + "-" + today_year
		sem = "SEM-2"
	print(cyea)

	return render_template('pdf.html',res1 = r,res2 = r1,x = x,date = d2,a = a,curr = cyea,sem=sem,co = co,co1 = co1,co2 = co2,co3 = co3)

@app.route('/upload/',methods = ['POST', 'GET'])
def upex():
	if request.method=='POST':
		f = request.files['ipfile']
		clg = request.form['clg']
		dept = request.form['dept']
		df = pd.read_excel(f)
		df2 = pd.DataFrame(df, columns = ['Teacher Name', 'Subject', 'Year', 'Division','Type(TH/PR)','Batch(if type is Prac)'])
		d1 = df2.fillna('-')
		c.execute('TRUNCATE table faculty')

		for index, row in df.iterrows():
			name = row["Teacher Name"].rstrip()
			sub = row["Subject"].rstrip()
			year = row["Year"].rstrip()
			div = row["Division"].rstrip()
			typ = row["Type(Theo/Prac)"].rstrip()
			batch = row["Batch(if type is Prac)"].rstrip()
			if name != '-':
				c.execute('insert into `faculty` (`college`,`dept`,`year`,`division`,`subject`,`subteacher`,`type`,`batch`) values(%s,%s,%s,%s,%s,%s,%s,%s)',(clg,dept,year,div,sub,name,typ,batch,))
				mydb.commit()
			res =((clg,dept),)
		alt = 'nik'
		return render_template('1111.html' ,alt =alt ,res =res)

@app.route('/elective/',methods = ['POST', 'GET'])
def elect():
	if request.method=='POST':
		f = request.files['ipfile']
		clg = request.form['clg']
		dept = request.form['dept']
		df = pd.read_excel(f)
		df2 = pd.DataFrame(df, columns = ['Teacher Name' , 'Elective-1' , 'Elective-2'])
		d1 = df2.fillna('-')
		c.execute('TRUNCATE table elective')

		for index, row in d1.iterrows():
			tea = row["Teacher Name"].rstrip()
			el1 = row["Elective-1"].rstrip()
			el2 = row["Elective-2"].rstrip()
			c.execute('insert into `elective` (`college`,`dept`,`teach`,`el1`,`el2`) values(%s,%s,%s,%s,%s)',(clg,dept,tea,el1,el2,))
			mydb.commit()
		res =((clg,dept),)
		alt = 'nik'
		return render_template('1111.html' ,alt =alt ,res =res)

@app.route('/count/',methods = ['POST', 'GET'])
def count():
	if request.method=='POST':
		f = request.files['ipfile']
		clg = request.form['clg']
		dept = request.form['dept']
		df = pd.read_excel(f)
		df2 = pd.DataFrame(df, columns = ['Year' , 'Division' , 'Count'])
		d1 = df2.fillna('-')
		c.execute('TRUNCATE table stcount')

		for index, row in d1.iterrows():
			yea = row["Year"].rstrip()
			div = row["Division"].rstrip()
			coun = row["Count"]

			c.execute('insert into `stcount` (`college`,`dept`,`year`,`div`,`count`) values(%s,%s,%s,%s,%s)',(clg,dept,yea,div,coun,))
			mydb.commit()
		res =((clg,dept),)
		alt = 'nik'
		return render_template('1111.html' ,alt =alt ,res =res)

@app.route('/elect/',methods = ['POST', 'GET'])
def elect1():
	if request.method=='POST':
		clg = request.form['clg']
		dept = request.form['dept']
		c.execute('select teach from elective where college = %s and dept = %s and teach != "-"',(clg,dept,))
		res3 = c.fetchall()

		c.execute('select el1 from elective where college = %s and dept = %s and el1 != "-"',(clg,dept,))
		res1 = c.fetchall()

		c.execute('select el2 from elective where college = %s and dept = %s and el2 != "-"',(clg,dept,))
		res2 = c.fetchall()
		return render_template('elect.html',res1 = res1,res2 = res2,res3 = res3)

@app.route('/blank/',methods = ['POST', 'GET'])
def blank():
	if request.method=='POST':
		return render_template('blank.html')

@app.route('/reset/',methods = ['POST', 'GET'])
def reset():
	if request.method=='POST':
		clg = request.form['reclg']
		dept = request.form['redept']

		print(clg + " " + dept)

		c.execute('delete from `feedcount` where `college` = %s and `dept` = %s',(clg,dept,))
		mydb.commit()
		return "hii"

if __name__=='__main__':
	app.secret_key='nikhil'
	#app.run(debug='true',threaded = 'true')
	serve(app, host='0.0.0.0', port=8000)
