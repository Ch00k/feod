from feod.model import db


class PriceCategory(db.Model):
    __tablename__ = 'price_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    
    price_subcategories = db.relationship('PriceSubCategory', backref = 'price_category')
    
    def __init__(self, id=None, name=None, active=None):
        self.id = id
        self.name = name
        self.active = active
        
    def __repr__(self):
        return '<PriceCategory %r>' % (self.id, self.name, self.active)

    
class PriceSubCategory(db.Model):
    __tablename__ = 'price_subcategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    last_update = db.Column(db.DateTime, nullable = False)
    price_category_id = db.Column(db.Integer, db.ForeignKey('price_category.id'))
                    
    def __init__(self, id=None, name=None, active=None, last_update=None, price_category_id=None):
        self.id = id
        self.name = name
        self.active = active
        self.last_update = last_update
        self.price_category_id = price_category_id
        
    def __repr__(self):
        return '<PriceSubCategory %r>' %(self.id, self.name, self.active, self.last_update, self.price_category_id)

    
class Price(db.Model):
    __tablename__ = 'price'
    code = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    title = db.Column(db.Text, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    price_subcategory_id = db.Column(db.Integer, db.ForeignKey('price_subcategory.id'))
    
    price_subcategory = db.relationship('PriceSubCategory', backref = db.backref('price_items'))
    
    def __init__(self, code=None, title=None, price=None, price_subcategory_id=None):
        self.code = code
        self.title = title
        self.price = price
        self.price_subcategory_id = price_subcategory_id
        
    def __repr__(self):
        return '<Price %r>' % (self.id, self.code, self.title, self.price, self.price_subcategory_id)

    
class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    inmenu = db.Column(db.Boolean, nullable = False)
    last_update = db.Column(db.DateTime, nullable = False)
    
    def __init__(self, id=None, title=None, content=None, inmenu=None, last_update=None):
        self.id = id
        self.title = title
        self.content = content
        self.inmenu = inmenu
        self.last_update = last_update
        
    def __repr(self):
        return '<Page %r>' % (self.id, self.title, self.content, self.inmenu, self. last_update)
