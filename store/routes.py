from store import app
from flask import render_template, redirect, url_for, flash
from store.models import User, ProductListing, Buyer, Address, ZipCodeInfo, Category, Seller, Credit_Cards
from store.forms import RegisterForm, LoginForm, ChangePasswordForm, ProductListingForm
from store import db
from flask_login import login_user, logout_user, login_required
import random
from datetime import datetime


# home page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# dynamic routing -> allows check info page of any user
@app.route('/info/<email>', methods=['get', 'post'])
@login_required
def info_page(email):
    # name, age, gender, addr_id's
    buyer_info = Buyer.query.filter_by(email=email).first()
    home_addr_id = buyer_info.homeAddrID
    billing_addr_id = buyer_info.billingAddrID

    # street name, number, and zipcode
    home_addr_info = Address.query.filter_by(id=home_addr_id).first()
    billing_addr_info = Address.query.filter_by(id=billing_addr_id).first()
    home_zipcode_id = home_addr_info.zipcode
    billing_zipcode_id = billing_addr_info.zipcode

    # city and state
    home_zipcode_info = ZipCodeInfo.query.filter_by(zipcode=home_zipcode_id).first()
    billing_zipcode_info = ZipCodeInfo.query.filter_by(zipcode=billing_zipcode_id).first()

    # credit card number(s)
    cc_info = Credit_Cards.query.filter_by(owner_email=email).all()

    return render_template('info.html',buyer_info=buyer_info, home_addr_info=home_addr_info,
                           billing_addr_info=billing_addr_info, home_zipcode_info=home_zipcode_info,
                           billing_zipcode_info=billing_zipcode_info, cc_info=cc_info)

# change password page and updates db w/ new password (hash function in models.User)
@app.route('/change-password/<email>', methods=['get', 'post'])
@login_required
def change_password_page(email):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user.check_password(attempt=form.password1.data):
            user.password = form.password2.data
            db.session.commit()
            flash(f'Success! You password has been changed', category='success')
            redirect(url_for('info_page', email=email))
        else:
            flash(f'Password not updated successfully!', category='danger')

    return render_template('changePassword.html', form=form)

# essentially an event handler for the "Remove" button on the Manage Product Listing Page
# no actual page here, simply an update step
@app.route('/remove/<listID>/<email>', methods=['get', 'post'])
@login_required
def remove_products(listID, email):
    # assigns a stop-time value to the db for a given product
    stop_time = datetime.now()
    product = ProductListing.query.filter_by(listID=listID).first()
    product.stop_time=stop_time
    db.session.commit()
    flash('Product removed successfully!', category='success')
    return redirect(url_for('manage_products_page', email=email))

# manage product listing page
@app.route('/manage-product-listing/<email>', methods=['get', 'post'])
@login_required
def manage_products_page(email):
    form = ProductListingForm()
    # affirm that user is an authorized seller
    seller = Seller.query.filter_by(email=email).first()
    if seller == None:
        flash("You are not an authorized seller for this store!", category='danger')
        return redirect(url_for('store_page'))

    if form.validate_on_submit():
        # check that category is valid
        category = Category.query.filter_by(name=form.category.data).first()
        if category == None:
            flash("Category does not exist!", category='danger')
        else:
            # create start time for new product listing
            starttime = datetime.now()
            # find a valid list ID for new product listing
            list_id = 1
            find_id = ProductListing.query.filter_by(listID=list_id).first()
            while (find_id != None):
                list_id = random.randint(1, 6000)
                find_id = ProductListing.query.filter_by(listID=list_id).first()
            # create new product listing
            new_listing = ProductListing(sellerEmail=email, listID=list_id, category=form.category.data,
                                         title=form.title.data,
                                         name=form.name.data, desc=form.desc.data, pricde=form.price.data,
                                         quantity=form.quantity.data, start_time=starttime)
            db.session.add(new_listing)
            db.session.commit()
            flash("New product listing created!", category='success')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating this listing: {err_msg}', category='danger')
    # determine active vs past products sold, keeps track of product listing timeline
    # active products have no stop time
    # removed products are identified by the existence of a 'stop_time'
    seller_products = ProductListing.query.filter_by(sellerEmail=email).all()
    active_products = []
    removed_products = []
    for prod in seller_products:
        if prod.stop_time == None:
            active_products.append(prod)
        else:
            removed_products.append(prod)

    return render_template('manageProducts.html', form=form, active_products=active_products,
                           removed_products=removed_products)

# ignore this next line -> handling some weird error
products = ProductListing.query.all()

# store page
@app.route('/store')
@app.route('/store/<category>')
@login_required
def store_page(category='Root'):
    # finds all children of the current category to display as a possible filter
    display_categories = Category.query.filter_by(parent=category).all()
    # added the stop_time=None to remove old products from store
    if category == 'Root':
        products = ProductListing.query.filter_by(stop_time=None).all()
    else:
        # pass in the category to the query to find more specific items
        products = ProductListing.query.filter_by(category=category, stop_time=None).all()
    return render_template('store.html', products=products, display_categories=display_categories)

# create account page -> have to extend to create buyers and sellers
# ONLY creates a User
@app.route('/register', methods=['get', 'post'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # if valid entries, add user to database
        user_to_create = User(email=form.email.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        # login the user
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as: {user_to_create.email}", category='success')
        # send to store page
        return redirect(url_for('store_page'))
    # if no errors
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating your account: {err_msg}', category='danger')
    return render_template('register.html', form=form)

# login page
@app.route('/login', methods=['get', 'post'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        is_user = User.query.filter_by(email=form.email.data).first()
        # if user exists and passwords match, login
        if is_user and is_user.check_password(attempt=form.password.data):
            login_user(is_user)
            flash(f'Success! You are logged in as: {is_user.email}', category='success')
            return redirect(url_for('store_page'))
        else:
            flash('The email and password you entered are not recognized! Please try again', category='danger')

    return render_template('login.html', form=form)

# logout handling
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have successfully signed out!', category='info')
    return redirect(url_for('login_page'))