import os
from feod.controllers import functions
from flask import request, redirect, url_for, render_template, session, flash
from werkzeug import secure_filename
from feod import app
from feod import ALLOWED_EXTENSIONS, ADMIN_USERNAME, ADMIN_PASSWORD, SECRET_KEY


@app.route('/admin/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != ADMIN_USERNAME or \
           request.form['password'] != ADMIN_PASSWORD:
            error = 'Invalid credentials'
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            flash('You were successfully logged in')
            return redirect(url_for('admin'))
        
    return render_template('admin/login.html', error = error)

@app.route('/admin/logout')
def logout():
    session.pop('username', None)
    flash('You were successfully logged out')
    
    return redirect(url_for('login'))

@app.route('/admin/')
@functions.login_required
def admin():
    return render_template('admin/admin.html')

@app.route('/admin/pages/', methods=['GET', 'POST'])
@functions.login_required
def pages():
    if request.method == 'POST':
        functions.delete_pages(request.form.getlist('do_delete'))
        flash('Pages deleted successfully')

    return render_template('admin/pages.html', pages = functions.get_pages())

@app.route('/admin/pages/new/', methods=['GET', 'POST'])
@functions.login_required
def add_page():
    error = None
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            error = 'Please provide title and content'
        else:
            inmenu = True if 'inmenu' in request.form else False
            functions.create_page(title = request.form['title'],
                                  content = request.form['content'],
                                  inmenu = inmenu)
            flash('Page created successfully')
            
            return redirect(url_for('pages'))
    
    return render_template('admin/add_page.html', error = error)

@app.route('/admin/pages/edit/<int:id>', methods = ['GET', 'POST'])
@functions.login_required
def edit_page(id):
    error = None
    if request.method == 'POST':
        inmenu = True if 'inmenu' in request.form else False
        if not request.form['title'] or not request.form['content']:
            error = 'Please provide title and content'
        else:
            functions.save_updated_page(id,
                                        request.form['title'],
                                        request.form['content'],
                                        inmenu)
            flash('Page saved successfully')
            return redirect(url_for('pages'))
        
    return render_template('admin/edit_page.html',
                           page = functions.get_page(id),
                           error = error)

@app.route('/admin/pages/delete/<int:id>')
@functions.login_required
def delete_page(id):
    functions.delete_page(id)
    flash('Page deleted successfully')
        
    return redirect(url_for('pages'))

@app.route('/admin/pages/<int:id>/')
@functions.login_required
def show_page(id):
    return render_template('admin/page.html',
                           page = functions.get_page(id))

@app.route('/admin/prices/')
@functions.login_required
def prices():
    return render_template('admin/prices.html')

@app.route('/admin/prices/categories', methods = ['GET', 'POST'])
@functions.login_required
def price_categories():
    cat_error = None
    subcat_error = None
    active = True if 'active' in request.form else False
    if request.method == 'POST':
        if request.form['hidden'] == 'addcat':
            if request.form['name']:
                functions.create_price_category(request.form['name'], active)
                flash('Price category created successfully')
            else:
                cat_error = 'Please provide price category name'
        elif request.form['hidden'] == 'addsubcat':
            if request.form['name']:
                functions.create_price_subcategory(request.form['name'], active, request.form['pcat'])
                flash('Price subcategory created successfully')
            else:
                subcat_error = 'Please provide price subcategory name'
        elif request.form['hidden'] == 'delete':
            functions.delete_price_categories(request.form.getlist('do_delete'))
            flash('Price categories deleted successfully')
                
    return render_template('admin/price_categories.html',
                           price_categories = functions.get_price_categories(),
                           price_subcategories = functions.get_price_subcategories(),
                           cat_error = cat_error,
                           subcat_error = subcat_error)

@app.route('/admin/prices/categories/delete/<int:id>')
@functions.login_required    
def delete_price_category(id):
    functions.delete_price_category(id)
    flash('Price category deleted successfully')
        
    return redirect(url_for('price_categories'))

@app.route('/admin/prices/subcategories/delete/<int:id>')
@functions.login_required
def delete_price_subcategory(id):
    functions.delete_price_subcategory(id)
    flash('Price catesubgory deleted successfully')
        
    return redirect(url_for('price_categories'))

@app.route('/admin/prices/subcategories/<int:subcategory_id>/addpricelist/', methods = ['GET', 'POST'])
@functions.login_required
def add_price_list(subcategory_id):
    if request.method == 'POST':
        error = None
        upload_file = request.files['file']
        if upload_file:
            if functions.check_allowed_file(upload_file.filename):
                filename = secure_filename(upload_file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'],
                                    filename)
                upload_file.save(os.path.join(path))
                functions.add_price_list(path, subcategory_id)
                return redirect(url_for('price_categories'))
            else:
                error = 'Files of this type are not allowed'
        else:
            error = 'Please select a file to upload'
    
    return render_template('admin/add_price.html', subcategory_id = subcategory_id)



"""
@app.route('/admin/prices/toner')
@functions.login_required
def price_toner():
    prices = get_prices(Toner)
    
    return render_template('admin/price_toner.html', prices = prices)
    
@app.route('/admin/prices/laser')
@functions.login_required
def price_laser():
    prices = get_prices(Laser)
    
    return render_template('admin/price_laser.html', prices = prices)
    
@app.route('/admin/prices/ink')
@functions.login_required
def price_ink():
    prices = get_prices(Ink)
    
    return render_template('admin/price_ink.html', prices = prices)

@app.route('/admin/prices/new/', methods=['GET', 'POST'])
@functions.login_required
def add_price():
    error = None
    if request.method == 'POST':
        upload_file = request.files['file']
        if upload_file:
            if allowed_file(upload_file.filename):
                filename = secure_filename(upload_file.filename)
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                              filename))
                if 'price_type' in request.form:
                    price_type = PRICES[request.form['price_type']]
                    write_price(filename, price_type = price_type)
                    return redirect(url_for('prices'))
                else:
                    error = 'Please select price type'
            else:
                error = 'Files of this type are not allowed'
        else:
            error = 'Please select a file to upload'
            
    return render_template('admin/add_price.html', error = error)
"""