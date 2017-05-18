# import webbrowser
import requests
import json


CLIENT_ID = ""
# REDIRECT_URI = ""
RAW_SCOPE = ["basic", "public_content", "comments", "relationships", "likes", "follower_list"]
scope = "+".join(RAW_SCOPE)


def authenticate():
    """
    webbrowser.open_new(
        "https://api.instagram.com/oauth/authorize/?client_id={}&redirect_uri={}&scope={}&response_type=token"
            .format(CLIENT_ID, REDIRECT_URI, scope))

    access_token = ""
    """

    return ""


def get_self_information(access_token, information):
    url = "https://api.instagram.com/v1/users/self/?access_token={}".format(access_token)

    data = json.loads(requests.get(url).text)
    data = data["data"]

    try:
        return data[information]
    except KeyError:
        print("Invalid field!")


if __name__ == "__main__":
    token = authenticate()
    print(get_self_information(token, input("What would you like to know about the user? ")))
