from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..main.forms import SearchSimple


@auth.route("/fileserver")
def nginx_auth():
    #print('who is it?')
    if current_user.is_authenticated and current_user.confirmed:
        return "You are logged in!"
    else:
        return 'Sorry, but unfortunately you\'re not logged in.', 401


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    
    
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():

        ##Simple search snippet to add to every view   methods=['GET', 'POST'])
    searchform= SearchSimple()
    if searchform.validate_on_submit() :
        searchstring=searchform.search.data
        session['search']=searchstring
        return redirect(url_for('tinylib.search',searchstring=searchstring,page=1, searchform=searchform ))


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form, searchform=searchform)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
        ##Simple search snippet to add to every view   methods=['GET', 'POST'])
    searchform= SearchSimple()
    if searchform.validate_on_submit() :
        searchstring=searchform.search.data
        session['search']=searchstring
        return redirect(url_for('tinylib.search',searchstring=searchstring,page=1, searchform=searchform ))


    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, searchform=searchform)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    
        ##Simple search snippet to add to every view   methods=['GET', 'POST'])
    searchform= SearchSimple()
    if searchform.validate_on_submit() :
        searchstring=searchform.search.data
        session['search']=searchstring
        return redirect(url_for('tinylib.search',searchstring=searchstring,page=1, searchform=searchform ))



    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form, searchform=searchform)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()

        ##Simple search snippet to add to every view   methods=['GET', 'POST'])
    searchform= SearchSimple()
    if searchform.validate_on_submit() :
        searchstring=searchform.search.data
        session['search']=searchstring
        return redirect(url_for('tinylib.search',searchstring=searchstring,page=1, searchform=searchform ))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            print(token)
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, searchform=searchform)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()

        ##Simple search snippet to add to every view   methods=['GET', 'POST'])
    searchform= SearchSimple()
    if searchform.validate_on_submit() :
        searchstring=searchform.search.data
        session['search']=searchstring
        return redirect(url_for('tinylib.search',searchstring=searchstring,page=1, searchform=searchform ))

    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form, searchform=searchform)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()

        ##Simple search snippet to add to every view   methods=['GET', 'POST'])
    searchform= SearchSimple()
    if searchform.validate_on_submit() :
        searchstring=searchform.search.data
        session['search']=searchstring
        return redirect(url_for('tinylib.search',searchstring=searchstring,page=1, searchform=searchform ))

    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form,  searchform=searchform)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
