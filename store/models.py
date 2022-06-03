from store import db, bcrypt, login_manager
from flask_login import UserMixin
# flask login manager requirement
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    email = db.Column(db.String(length=50), primary_key=True)
    # password will be hashed to 60 chars w/ SQLAlchemy
    password_hash = db.Column(db.String(length=60), nullable=False)
    # property for UserMixin -> needs dedicated 'id attribute'
    @property
    def id(self):
        return self.email
    # allows us to pass in a 'password' to later be stored as a password hash
    @property
    def password(self):
        return self.password
    # take in password and store as a password hash
    @password.setter
    def password(self, plain_txt):
        self.password_hash = bcrypt.generate_password_hash(plain_txt).decode('utf-8')
    # checks an incoming plain-text password against the password_hash
    def check_password(self, attempt):
        return bcrypt.check_password_hash(self.password_hash, attempt)


class Address(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    zipcode = db.Column(db.Integer())
    street_num = db.Column(db.Integer(), nullable=False)
    street_name = db.Column(db.String(20), nullable=False)

class ZipCodeInfo(db.Model):
    zipcode = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    state_id = db.Column(db.String(2), nullable=False)

class Credit_Cards(db.Model):
    cc_num = db.Column(db.String(20), primary_key=True)
    card_code = db.Column(db.Integer(), nullable=False)
    expire_month = db.Column(db.Integer(), nullable=False)
    expire_year = db.Column(db.Integer(), nullable=False)
    card_type = db.Column(db.String(20), nullable=False)
    owner_email = db.Column(db.String(30))

class Buyer(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    gender = db.Column(db.String(50)) #change this to ENUM?
    age = db.Column(db.SMALLINT)
    homeAddrID = db.Column(db.INTEGER)
    billingAddrID = db.Column(db.INTEGER)

class Seller(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    routNum = db.Column(db.String(50))
    accNum = db.Column(db.INTEGER)
    bal = db.Column(db.INTEGER)

class LocalVendor(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    busiName = db.Column(db.String(50))
    busiAddrID = db.Column(db.INTEGER)
    busiPhone = db.Column(db.String(50))

class Category(db.Model):
    parent = db.Column(db.String(50))
    name = db.Column(db.String(50),primary_key=True)

class ProductListing(db.Model):
    listID = db.Column(db.INTEGER, primary_key=True)
    sellerEmail = db.Column(db.String(50))
    category = db.Column(db.String(50))
    title = db.Column(db.String(50))
    name = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    pricde = db.Column(db.String(10))
    quantity = db.Column(db.INTEGER)
    start_time = db.Column(db.DateTime, nullable=True)
    stop_time = db.Column(db.DateTime, nullable=True)



class Order(db.Model):
    transID = db.Column(db.INTEGER, primary_key=True)
    sellerEmail = db.Column(db.String(50))
    listID = db.Column(db.INTEGER)
    buyerEmail = db.Column(db.String(50))
    date = db.Column(db.String(50))
    quantity = db.Column(db.INTEGER)
    payment = db.Column(db.String(50))

class Review(db.Model):
    sellerEmail = db.Column(db.String(50), primary_key=True)
    buyerEmail = db.Column(db.String(50), primary_key=True)
    listID = db.Column(db.INTEGER, primary_key=True)
    desc = db.Column(db.String(200))

class Rating(db.Model):
    sellerEmail = db.Column(db.String(50), primary_key=True)
    buyerEmail = db.Column(db.String(50), primary_key=True)
    date = db.Column(db.String(50), primary_key=True)
    rating = db.Column(db.INTEGER)
    desc = db.Column(db.String(200))


db.create_all()
'''
# script for filling in the database w/ provided csv files

import csv, sqlite3

# populate Category
file = open('Categories.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Category(parent=item[0], name=item[1])
    db.session.add(x)
    db.session.commit()

# populate Credit Cards
file = open('Credit_Cards.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Credit_Cards(cc_num=item[0], card_code=item[1], expire_month=item[2], expire_year=item[3], card_type=item[4],
                     owner_email=item[5])
    db.session.add(x)
    db.session.commit()

# populate ZipCodeInfo
file = open('ZipCode_Info.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = ZipCodeInfo(zipcode=item[0], city=item[1], state_id=item[2])
    db.session.add(x)
    db.session.commit()

# populate Buyer
file = open('Buyers.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Buyer(email=item[0], firstName=item[1], lastName=item[2], gender=item[3],
              age=item[4], homeAddrID=item[5], billingAddrID = item[6])
    db.session.add(x)
    db.session.commit()

# populate Address
file = open('Address.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Address(id=item[0], zipcode=item[1], street_num=item[2], street_name=item[3])
    db.session.add(x)
    db.session.commit()

# populate Seller
file = open('Sellers.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Seller(email=item[0], routNum=item[1], accNum=item[2], bal=item[3])
    db.session.add(x)
    db.session.commit()

# populate Local Vendors
file = open('Local_Vendors.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = LocalVendor(email=item[0], busiName=item[1], busiAddrID=item[2], busiPhone=item[3])
    db.session.add(x)
    db.session.commit()

# populate Product LIsting
file = open('Product_Listing.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    if item[2] == 'iPhone':
        item[2] = 'Cell Phones'
    x = ProductListing(listID=item[1], sellerEmail=item[0], category=item[2].title(), title=item[3], name=item[4],
                       desc=item[5], pricde=item[6], quantity=item[7])
    db.session.add(x)
    db.session.commit()

# populate Orders
file = open('Orders.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Order(transID=item[0], sellerEmail=item[1], listID=item[2], buyerEmail=item[3], date=item[4],
              quantity=item[5], payment=item[6])
    db.session.add(x)
    db.session.commit()

# populate Reviews
file = open('Reviews.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Review(sellerEmail=item[0], buyerEmail=item[1], listID=item[2], desc=item[3])
    db.session.add(x)
    db.session.commit()

# populate Rating
file = open('Ratings.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = Rating(sellerEmail=item[0], buyerEmail=item[1], date=item[2], rating=item[3], desc=item[4])
    db.session.add(x)
    db.session.commit()

# populate User
file = open('Users.csv')
contents = csv.reader(file)
next(contents)
for item in contents:
    x = User(email=item[0], password=item[1])
    db.session.add(x)
    db.session.commit()

'''