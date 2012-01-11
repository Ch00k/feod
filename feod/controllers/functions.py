import datetime
from functools import wraps
from flask import request, session, redirect, url_for
from feod import ALLOWED_EXTENSIONS
from feod.model import db
import xlrd
from feod.model.database import PriceCategory, PriceSubCategory, Price, Page

class XLSReader(object):
    def __init__(self, input_file):
        self.xls = xlrd.open_workbook(input_file)
        
    def read(self):
        sh = self.xls.sheet_by_index(0)
        data = []
        for row in range(10, sh.nrows):
            values = []
            for col in range(1, sh.ncols):
                if ((col != 3) & (col != 4)):
                    values.append(sh.cell(row,col).value)
            data.append(values)
        
        return data
        
def check_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def create_page(title, content, inmenu):
    page = Page(title = title,
                content = content,
                inmenu = inmenu,
                last_update = datetime.datetime.now())
    db.session.add(page)
    db.session.commit()
    db.session.close()
    
def save_updated_page(id, title, content, inmenu):
    db.session.query(Page).filter(Page.id == id).update({'title': title,
                                                         'content': content,
                                                         'updated': datetime.datetime.now(),
                                                         'inmenu': inmenu})
    db.session.commit()
    db.session.close()
    
def delete_page(id):
    db.session.query(Page).filter(Page.id == id).delete()
    db.session.commit()
    db.session.close()
    
def delete_pages(ids):
    db.session.query(Page).filter(Page.id.in_(ids)).delete(synchronize_session='fetch')
    db.session.commit()
    db.session.close()
    
def get_pages():
    return db.session.query(Page)

def get_page(id):
    return db.session.query(Page).filter(Page.id == id)

def create_price_category(name, active):
    price_category = PriceCategory(name = name,
                                   active = active)
    db.session.add(price_category)
    db.session.commit()
    db.session.close()
    
def delete_price_categories(ids):
    db.session.query(PriceCategory).filter(PriceCategory.id.in_(ids)).delete(synchronize_session='fetch')
    db.session.commit()
    db.session.close()
    
def create_price_subcategory(name, active, price_category_id):
    price_subcategory = PriceSubCategory(name = name,
                                         active = active,
                                         last_update = datetime.datetime.now(),
                                         price_category_id = price_category_id)
    db.session.add(price_subcategory)
    db.session.commit()
    db.session.close()
    
def create_price_list(code, title, price, price_subcategory_id):
    price = Price(code = code,
                  title = title,
                  price = price,
                  price_subcategory_id = price_subcategory_id)
    db.session.add(price)
    db.session.commit()
    db.session.close()
    
def get_price_categories():
    return db.session.query(PriceCategory)

def get_price_subcategories():
    return db.session.query(PriceSubCategory)

def delete_price_category(id):
    db.session.query(PriceCategory).filter(PriceCategory.id == id).delete()
    db.session.commit()
    db.session.close()
    
def delete_price_subcategory(id):
    db.session.query(PriceSubCategory).filter(PriceSubCategory.id == id).delete()
    db.session.commit()
    db.session.close()
    
def get_existing_price_list_records(subcategory_id):
    codes = []
    for record in db.session.query(Price, Price.code).filter(Price.price_subcategory_id == subcategory_id):
        codes.append(record.code)
        
    return codes
        
def add_price_list(filename, subcategory_id):
    data = XLSReader(filename).read()
    error = None
    for row in data:
        record = Price(code = row[0],
                       title = row[1],
                       price = row[2],
                       price_subcategory_id = subcategory_id)
        if row[0] not in get_existing_price_list_records(subcategory_id):
            db.session.add(record)
        else:
            for code in get_existing_price_list_records(subcategory_id):
                if row[0] == code:
                    db.session.query(Price).filter(Price.code == code).update({'title': row[1], 'price': row[2]})
    db.session.commit()
    db.session.close()



"""
def check_duplicates(filename):
    data = read(filename)
    codes = []
    for row in data:
        codes.append(row[0])
    dupes = [code for code in codes if codes.count(code) > 1]
    if len(dupes) != 0:
        return True
    
    return False
"""
