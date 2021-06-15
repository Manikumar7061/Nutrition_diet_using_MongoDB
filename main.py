from flask import Flask, render_template,request,redirect,url_for,session,flash # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import bcrypt 
import os

app = Flask(__name__)

title = "NoSQL Project Application"
heading = "Nutrition-overview "

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.foods    #Select the database
todos = db.review #Select the collection name
users= db.admin
customers=db.users
carted=db.carted

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')
#logins



'''
@app.before_request
def before_request():
    if 'username' in session:
       return render_template('home.html' , username=session['username'])

   

@app.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    users = logins
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        if login_user['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect('home.html')

    flash( 'Invalid username/password combination')
    return render_template('loginindex.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = logins
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
           # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect("/loginuser")
        
        return 'That username already exists!'

    return render_template('register.html')

*/'''
   # End of logins
   # login
@app.route('/')
def index():
    if 'username' in session:
        return redirect('/uncompleted')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    #users = db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if (request.form['pass'] == login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        #users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('home.html',a1=a1,todos=todos_l,t=title,h=heading)

#@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
        
	todos_l = todos.find({"done":"no"})
	a2="active"
	return render_template('home.html',a2=a2,todos=todos_l,t=title,h=heading)
  

@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('userhome.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	food_group=request.values.get("food_group")
	calories=request.values.get("calories")
	fat=request.values.get("fat")
	protein=request.values.get("protein")
	carbohydrates=request.values.get("carbohydrates")
	sat_fat=request.values.get("sat_fat")
	fiber=request.values.get("fiber")
	todos.insert({ "name":name, "food_group":food_group, "calories":calories, "fat":fat, "protein":protein, "carbohydrates":carbohydrates, "sat_fat":sat_fat, "fiber":fiber})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/list")
    

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	food_group=request.values.get("food_group")
	calories=request.values.get("calories")
	fat=request.values.get("fat")
	protein=request.values.get("protein")
	carbohydrates=request.values.get("carbohydrates")
	sat_fat=request.values.get("sat_fat")
	fiber=request.values.get("fiber")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "food_group":food_group, "calories":calories, "fat":fat, "protein":protein, "carbohydrates":carbohydrates, "sat_fat":sat_fat, "fiber":fiber}})
	return redirect("/list")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
                
		counted = todos.find({refer:key}).count()
	return render_template('searchlist.html',todos=todos_l,c=counted,t=title,h=heading)
@app.route('/user')
def to_user ():
	return render_template('userhome.html')
################################################################
    ########### customer #################
@app.route('/customerindex')
def customerindex():
    if 'customer' in session:
        return redirect('/customerlist')

    return render_template('userindex.html')

@app.route('/customerlogin', methods=['POST'])
def customerlogin():
    #customers = db.customers
    login_user = customers.find_one({'name' : request.form['customer']})

    if login_user:
        if (request.form['customerpass'] == login_user['password']):
            session['customer'] = request.form['customer']
            return redirect(url_for('customerindex'))

    return 'Invalid username/password combination'

@app.route('/customerregister', methods=['POST', 'GET'])
def customerregister():
    if request.method == 'POST':
        #customers = db.customers
        existing_user = customers.find_one({'name' : request.form['customer']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            customers.insert({'name' : request.form['customer'], 'password' : request.form['customerpass']})
            session['customer'] = request.form['customer']
            return redirect(url_for('customerindex'))
        
        return 'That username already exists!'

    return render_template('userregister.html')
@app.route('/customerlogout')
def customerlogout():
    session.pop('customer', None)
    return redirect('/')

@app.route("/customerlist")
def customerlists ():
	#Display the all Tasks
	todos_l = todos.find()
	a4="active"
	return render_template('userhome.html',a4=a4,todos=todos_l,t=title,h=heading)

#@app.route("/")
@app.route("/customeruncompleted")
def customertasks ():
    todos_l = todos.find({"done":"no"})
    carted_list = carted.find({"UID":session['customer']})
    c=carted.find({"UID":session['customer']}).count()
    
    a5="active"
    return render_template('userhome.html',a5=a5,todos=todos_l,count=c,carted=carted_list,t=title,h=heading)
    

  
#add cart data to db.
@app.route('/cart')
def cart():
    id=request.values.get("_id")
    task=todos.find_one({"_id":ObjectId(id)})
    #for i in task:
    carted.insert({  "UID":session['customer'], "name":task['name'] , "food_group": task['food_group'] , "calories": task['calories'] , "fat": task['fat'] , "protein": task['protein'] , "carbohydrates": task['carbohydrates'] , "sat_fat": task['sat_fat'] , "fiber": task['fiber'] })
    return redirect('/customerlist')


@app.route("/customerremove")
def customerremove ():
	#Deleting a Task with various references
	id=request.values.get("_id")
	task=carted.find_one({"_id":ObjectId(id)})
	carted.remove({"_id":task['_id']})
	return redirect("/customeruncompleted")
'''
@app.route("/completed")
def customercompleted ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a6="active"
	return render_template('userhome.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/customerdone")
def customerdone ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/customeraction", methods=['POST'])
def customeraction ():
	#Adding a Task
	name=request.values.get("name")
	food_group=request.values.get("food_group")
	calories=request.values.get("calories")
	fat=request.values.get("fat")
	protein=request.values.get("protein")
	carbohydrates=request.values.get("carbohydrates")
	sat_fat=request.values.get("sat_fat")
	fiber=request.values.get("fiber")
	todos.insert({ "name":name, "food_group":food_group, "calories":calories, "fat":fat, "protein":protein, "carbohydrates":carbohydrates, "sat_fat":sat_fat, "fiber":fiber})
	return redirect("/customerlist")'''


    

'''@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	food_group=request.values.get("food_group")
	calories=request.values.get("calories")
	fat=request.values.get("fat")
	protein=request.values.get("protein")
	carbohydrates=request.values.get("carbohydrates")
	sat_fat=request.values.get("sat_fat")
	fiber=request.values.get("fiber")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "food_group":food_group, "calories":calories, "fat":fat, "protein":protein, "carbohydrates":carbohydrates, "sat_fat":sat_fat, "fiber":fiber}})
	return redirect("/list")
'''
@app.route("/customersearch", methods=['GET'])
def customersearch():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
                
		counted = todos.find({refer:key}).count()
	return render_template('usersearchlist.html',todos=todos_l,c=counted,t=title,h=heading)
if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run()

