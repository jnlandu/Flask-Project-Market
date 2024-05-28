from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, PurchaseItemForm, SellItemForm ## to import the class Register
from market import db
from market.forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/')
@app.route('/home') 
def home():
    return render_template('home.html')

# @app.route('/about')
# def about_page():
#     return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    selling_form = SellItemForm()
    purchase_form = PurchaseItemForm()
  
    if request.method == 'POST':
        #  Purchase item logic
        purchase_item = request.form.get('purchased_item')
        purchase_item_object = Item.query.filter_by(name = purchase_item).first()
        if purchase_item_object:
            if current_user.can_purchase(purchase_item_object):
                purchase_item_object.owner = current_user.id # assign the owner the id of the user
                current_user.budget -= purchase_item_object.price
                db.session.commit()
                # db.session.close()
                flash(f'Congratulations you purchased { purchase_item_object.name } for {purchase_item_object.price}', category='sucess')
            else:
                flash(f"Unfortunately, you don't have enought money to purchase { purchase_item_object.name } ", category='danger')
        #  Sell item logic
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name = sold_item).first()
        #  Test of the logged in user has really the ownership on the Item

        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f" Congratulations! You sold  { sold_item_object.name } iback in the market for {sold_item_object.print}", category='success')
            
            else:
                flash(f"Something went wrong with { sold_item_object.name }", category='danger')
        #  To remove the form resubmission
        return redirect(url_for('market_page'))
    if request.method == 'GET':

            items = Item.query.filter_by(owner = None) 
            owned_items = Item.query.filter_by(owner= current_user.id)

            return render_template('market.html', items= items, purchase_form= purchase_form, owned_items = owned_items, selling_form = selling_form)


@app.route('/register', methods =['GET','POST'])
def register_page():
    try:
        form = RegisterForm()
        ## from chatgpt
        # data_request = request.get_json()
        if form.validate_on_submit():
            user_to_create = User(username = form.username.data,
                                email_address = form.email_address.data,
                                password= form.password1.data)
            # with app.app_context():
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f'Account created successuffly! You are now logged in as : {user_to_create.username} ', category = 'success')
            # return redirect(url_for('market_page'))
            return redirect(url_for('market_page'))
        #  Check the erros arising from the validations
        if form.errors !={}: 
            for err_msg in form.errors.values():
                flash(f"There was an error with creating a user:{err_msg}")
   
   
    except:
        db.session.rollback()
        flash('An error occured when creating the account')
    finally:
        db.session.close()
    return render_template('register.html', form = form, category = "Danger")

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = LoginForm()
    if login.validate_on_submit():
        attempted_user = User.query.filter_by(username=login.username.data).first()
        #  Check if none
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=login.password.data):
            login_user(attempted_user)
            flash(f'Success! Your are logged as : {attempted_user.username} ', category = 'success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again.', category= 'danger')
    return render_template('login.html', form = login)



@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home'))

