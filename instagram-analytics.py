"""
Instagram Analytics

A console application utilizing the Instagram API to analyse user posts and more.

Colin Shum
Raymond Truong
"""

from datetime import datetime
import requests
import json


CLIENT_ID = "518e5f658324474cbc15c941ca0ee7ec"
REDIRECT_URI = "http://google.ca"
RAW_SCOPE = ["basic", "public_content", "comments", "relationships", "likes", "follower_list"]
SCOPE = "+".join(RAW_SCOPE)


class Post:
    """ A photo or video, generalized as a Post.
    """
    def __init__(self, data):
        """ Initialize a new Post self.

        @type self: Post
        @type data: Dict[lots of stuff]
        @rtype: None
        """
        self.id = data["id"]
        self.url = data["images"]["standard_resolution"]["url"]
        self.caption = data["caption"]["text"] if data["caption"] is not None else "* no caption *"
        self.likes = data["likes"]["count"]
        self.likers = []
        self.date = datetime.fromtimestamp(float(data["created_time"]))

    def __str__(self):
        """ Return a user-friendly representation of self.

        @type self: Post
        @rtype: str
        """
        return ("Caption: {} \n"
                "\t Likes: {} \n"
                "\t Post date: {} \n"
                .format(self.caption, self.likes, self.date))

    def __lt__(self, other):
        """ Return whether or not self is less than other. A Post is considered "less than" another Post if it has a
        lower number of likes. Allows for sorting of Posts by number of likes.

        @type self: Post
        @type other: Post
        @rtype: bool
        """
        return self.likes < other.likes


class User:
    """ A User.
    """
    def __init__(self, data):
        """ Initialize a new User self.

        @type self: User
        @type data: Dict[lots of stuff]
        @rtype: None
        """
        self.id = data["id"]
        self.username = data["username"]
        self.name = data["full_name"]
        self.media = data["counts"]["media"]
        self.following = data["counts"]["follows"]
        self.followers = data["counts"]["followed_by"]

    def __str__(self):
        """ Return a user-friendly representation of self.

        @type self: User
        @rtype: str
        """
        return ("Username: {} \n"
                "\t Name: {} \n"
                "\t Following / followers: {} / {} \n"
                .format(self.username, self.name, self.following, self.followers))


#TODO: implement this
def authenticate():
    """ Authenticate the user using a new browser window and return their access token.

    @rtype: str
    """
    return input("Enter your access token: ")


def get_media(access_token):
    """ Return a list of the user's Posts.

    @type access_token: str
    @rtype: List[Post]
    """
    url = "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(access_token)
    data = json.loads(requests.get(url).text)["data"]

    media = []
    for m in data:
        media.append(Post(m))

    return media


if __name__ == "__main__":
    token = authenticate()

    # print info about the user
    url = "https://api.instagram.com/v1/users/self/?access_token={}".format(token)
    data = json.loads(requests.get(url).text)["data"]
    self = User(data)
    print(self)

    # print all of their posts
    posts = get_media(token)
    sorted_posts = sorted(posts)
    for post in sorted_posts:
        print(post)
