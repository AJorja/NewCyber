from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, logout_user, login_required



app = Flask(__name__)
app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)  # creates the db object using the configuration
login = LoginManager(app)
login.login_view = 'login'

from forms import ContactForm, RegistrationForm, LoginForm, ResetPasswordForm
from models import Contact, User, Challenge


@app.route('/')
def homepage():  
    return render_template("index.html", title="Homepage", user=current_user)

@app.route('/leaderboard')
def leaderboard():
    # Example: get top 10 users sorted by score descending
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template("leaderboard.html", title="Leaderboard", users=users, user=current_user)

@app.route('/about')
def about():  
    return render_template("about.html", title="About Us", user=current_user)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        flash("Your message has been sent to administrators.")
        return redirect(url_for("homepage"))
    return render_template("contact.html", title="Contact Us", form=form, user=current_user)


@app.route('/photogallery') 
def photogallery(): 
    return render_template("photogallery.html", title="Photo Gallery", user=current_user)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email_address=form.email_address.data, name=form.name.data, user_level=1, active=True) # defaults to regular user
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("homepage"))
    return render_template("register.html", title="User Registration", form=form, user=current_user)

@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        print(user)
        if user is not None and user.check_password(form.password.data) or not user.active:
            # User has been authenticated
            login_user(user)
            print("DEBUG: Login Successful")
            return redirect(url_for("homepage"))
        else:
            print("DEBUG: Login Failed")
            # Username or password incorrect
            return redirect(url_for("login"))
    return render_template("login.html", title="Login", form=form, user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash("You Have Successfully Logged Out")
    return redirect(url_for("homepage"))

@app.route('/passwordreset', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=current_user.email_address).first()
        user.set_password(form.new_password.data)
        db.session.commit()
        flash("Your password has been changed.")
        return redirect(url_for('homepage'))
    return render_template("passwordreset.html", title='Reset Password', form=form, user=current_user)

@app.route('/challenges')
def challenges():
    challenges_list = Challenge.query.all()
    return render_template("challenges.html", title="Challenges", challenges=challenges_list, user=current_user)


@app.route('/challenge/<int:challenge_id>', methods=['GET', 'POST'])
@login_required  # Require login to submit flags and earn points
def challenge_page(challenge_id):
    from models import Challenge, User  # local import if needed

    challenge = Challenge.query.get_or_404(challenge_id)
    message = None

    if request.method == 'POST':
        submitted_flag = request.form.get('flag')

        if submitted_flag == challenge.flag:
            message = "🎉 Correct flag! Challenge complete."

            # Example: add points to user, adjust as needed
            current_user.score = (current_user.score or 0) + 10
            db.session.commit()

            flash(message, 'success')
        else:
            message = "❌ Incorrect flag, try again."
            flash(message, 'danger')

    return render_template('turbine.html', challenge=challenge, message=message, user=current_user)






@app.route('/rules')
def rules():
    # Just render the rules template for now
    return render_template("rules.html", title="Rules", user=current_user)


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", user=current_user), 500

@app.route('/contact_messages')
@login_required
def view_contact_messages():
 if current_user.is_admin():
    contact_messages = Contact.query.all()
    return render_template("contactMessages.html", title="Contact Messages", user=current_user, messages=contact_messages)
 else:
    return redirect(url_for("homepage"))
 
@app.route('/admin/list_all_users')
@login_required
def list_all_users():
    if current_user.is_admin():
        all_users = User.query.all()
        return render_template("listAllUsers.html", title="All Active Users", user=current_user, users=all_users)
    else:
        flash("You must be an administrator to access this functionality.")
        return redirect(url_for("homepage"))
    
@app.route('/reset_password/<userid>', methods=['GET', 'POST'])
@login_required
def reset_user_password(userid):
    form = ResetPasswordForm()
    user = User.query.filter_by(id=userid).first()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password has been reset for user {}'.format(user.name))
        return redirect(url_for('homepage'))
    return render_template("passwordreset.html", title='Reset Password', form=form, user=user)

@app.route('/admin/user_enable/<userid>')
@login_required
def user_enable(userid):
    user = User.query.filter_by(id=userid).first()
    user.active = not user.active
    db.session.commit()
    return redirect(url_for("list_all_users"))

if __name__ == '__main__':
    app.run()
