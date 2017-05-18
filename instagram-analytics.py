"""
Instagram Analytics

A console application utilizing the Instagram API to analyse user posts and more.

Colin Shum
Raymond Truong
"""


import webbrowser
import requests
import json


CLIENT_ID = "518e5f658324474cbc15c941ca0ee7ec"
REDIRECT_URI = "http://google.ca"
RAW_SCOPE = ["basic", "public_content", "comments", "relationships", "likes", "follower_list"]
scope = "+".join(RAW_SCOPE)


class Post:
    """ A photo or video, generalized as Post.

    === Attributes ===
    @type id: str
    @type url: str
    @type caption: str
    @type likes: int
    @type likers: List[User]
    """
    def __init__(self, data):
        """ Initialize a new Post self.

        @type self: Post
        @type data: Dict[lots of stuff]
        """
        self.id = data["id"]
        self.url = data["images"]["standard_resolution"]["url"]
        self.caption = data["caption"]["text"] if data["caption"] is not None else "* no caption *"
        self.likes = data["likes"]["count"]
        self.likers = []

    def __str__(self):
        """ Return a user-friendly representation of self.

        @type self: Post
        @rtype: str
        """
        return "Likes: {} / Caption: {}".format(self.likes, self.caption)

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

    === Attributes ===
    @type id: int
    @type username: str
    @type name: str
    @type bio: str
    @type following: int
    @type followers: int
    """
    def __init__(self):
        """ Initialize a new User self.

        @type self: User
        @rtype: None
        """
        self.id, self.following, self.followers = -1, -1, -1
        self.username, self.name, self.bio = "", "", ""


#TODO: implement this
def authenticate():
    """ Authenticate the user using a new browser window and return their access token.

    @rtype: str
    """
    # webbrowser.open_new(
    #     "https://api.instagram.com/oauth/authorize/?client_id={}&redirect_uri={}&scope={}&response_type=token"
    #         .format(CLIENT_ID, REDIRECT_URI, scope))
    #
    # access_token = "???"

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

    posts = get_media(token)
    sorted_posts = sorted(posts)
    for post in sorted_posts:
        print(post)
