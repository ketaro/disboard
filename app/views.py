from flask import render_template, flash, redirect, session, request, g, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms.main import LoginForm, SignupForm
from app.model import User
from app.helpers import hash_password, flash_errors
from sqlalchemy.exc import IntegrityError

import json
import datetime
import time

@app.before_request
def check_login():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    
    return render_template('500.html'), 500


@app.route("/")
@app.route('/index')
def index():
    if g.user is not None and g.user.is_authenticated() and g.user.is_admin():
        return redirect(url_for('game_list'))
    
    return render_template("index.html",
                title = 'Welcome')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# Create the user session
def setup_user_session(user, remember_me):
    session['admin'] = True
    session['role']   = None
    user.last_login = int(time.time())
    try:
        db.session.commit()
    except:
        print "[setup_user_session] Error setting last login"

    login_user(user, remember_me)
    

@app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    
    form = LoginForm(csrf_enabled=False)

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        
        # Login from user database
        user = User.query.filter_by(email=form.email.data, 
                                    password=hash_password(form.password.data)).first()
        
#             print "found ", user
#             print "email ", form.email.data
#             print "pwhash ", hash_password(form.password.data)
        
        if user:
            setup_user_session(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('game_list'))
                            
        else:
            session['user_id'] = None
            flash('User not found with that id/password.')
    
    # If there were validation errors, flash them to the view
    flash_errors(form)
    
    return render_template("/login.html", title="Login", 
                            form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('/about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    del g.user
    
    form = SignupForm()
    
    if form.validate_on_submit():
        # Create a new user and organization
        user = User(givenname=form.givenname.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    created_by=form.email.data,
                    updated_by=form.email.data,
                    created_at=int(time.time()),
                    updated_at=int(time.time())
                    )
        user.password = hash_password(form.password.data)
        if form.accept_tos.data:
            user.tos_agree = int(time.time())

        db.session.add(user)
        
        try:
            db.session.commit()

            flash("Welcome!  Please check your email for a confirmation message.")
            return redirect(url_for('game_list'))

        except IntegrityError as e:
            reason = e.message
            
            flash(reason)
    
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
    
    return render_template("signup.html",
                           title="Registration",
                           form=form)


