from flask import render_template,request,Blueprint
from dawgblawg.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view. Uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('home.html',blog_posts=blog_posts)
