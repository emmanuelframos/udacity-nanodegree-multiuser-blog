from handler.base import BlogHandler
from entities.post import Post
from entities.user import User
from entities.comment import Comment


class MainHandler(BlogHandler):
    """
    Class that handles main route
    """

    @BlogHandler.is_authenticated
    def get(self):
        """
        Redirect to main route id user is authenticated (sending posts and 
        user login as parameters), if no redirects to login route
        :return: 
        """
        user_id = self.request.cookies.get('user_id')
        posts = Post.get_posts()

        for post in posts:
            post.owner = User.get_by_hash(user_id)
            post.is_author = \
                post.author == self.request.cookies.get('user_desc')
            post.liked = self.request.cookies.get('user_desc') in post.likes

            comments = Comment.get_by_post_id(post.key.id())

            for comment in comments:
                comment.is_author = \
                    comment.author == self.request.cookies.get('user_desc')

            post.comments = comments

        self.render('main.html', posts=posts,
                    user=self.request.cookies.get('user_desc'))