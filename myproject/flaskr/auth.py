import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import os
from flask_mail import Mail, Message
mail = Mail()
import itsdangerous
serializer = itsdangerous.URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
from dotenv import load_dotenv
load_dotenv()


bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        error = None

        # Busca el usuario por correo electrónico
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = 'No user found with this email.'
        else:
            # Genera un token con una duración limitada
            token = serializer.dumps(email, salt='password-reset-salt')

            # Enviar un correo electrónico con el token
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            message = Message(
                "Reset Your Password",
                sender="noreply@example.com",
                recipients=[email],
                body=f"Click the following link to reset your password: {reset_url}",
            )
            mail.send(message)

            flash("An email with instructions to reset your password has been sent.")
            return redirect(url_for('auth.login'))

        if error:
            flash(error)

    return render_template('auth/forgot_password.html')  # Plantilla para solicitar el correo

@bp.route('/reset-password/<token>', methods=('GET', 'POST'))
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token válido por 1 hora
    except itsdangerous.SignatureExpired:
        flash("The password reset link has expired.")
        return redirect(url_for('auth.forgot_password'))
    except itsdangerous.BadSignature:
        flash("Invalid password reset link.")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        db = get_db()
        db.execute('UPDATE user SET password = ? WHERE email = ?', (generate_password_hash(password), email))
        db.commit()

        flash("Your password has been reset successfully.")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')  # Plantilla para ingresar nueva contraseña
