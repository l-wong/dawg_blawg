from dawgblawg import db
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dawgblawg.models import User, BlogPost
from dawgblawg.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from dawgblawg.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Registration Complete!")
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #checks password is correct and user exists
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged in Successfully!")
            #grab user's requested page - only used if user tries to access a page that they
            #have to be logged in to view. If they are going to a page that doesn't require login access
            #it would be set to none
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for("core.index")
            return redirect(next)
    return render_template('login.html',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

# account (update UserForm)
@users.route("/account", methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    profile_image = url_for('static',filename='profile_pics/'+ current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)


@users.route("/<username>")
def user_posts(username):
    #grab blog posts associated with users
    page = request.args.get('page',1,type=int) #cycle through user posts using pages
    user = User.query.filter_by(username=username).first_or_404() #returns 404 page if user doesnt exist
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)
