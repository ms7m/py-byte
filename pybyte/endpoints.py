

base = "https://api.byte.co"
def return_like(string):
    return base + f"/post/id/{string}/feedback/like"

def return_unrebyte(string):
    return base + f"/post/id/{string}/rebyte"

def return_comment(string):
    return base + f"/post/id/{string}/feedback/comment"

def return_follow(string):
    return base +  f"/account/id/{string}/follow"

class Endpoints:
    GOOGLE_LOGIN = base + "/authenticate/google"
    ACCOUNT = base + "/account/me"
    USERNAME_CHECK = base + "/"
    OTHER_ACCOUNT = base + "/account/id/"
    POST_INFO = base + "/post/id/"
    REBYTE = base + "/rebyte"
    UNREBYTE = return_unrebyte
    COMMENT = return_comment
    LIKE = return_like
    FOLLOW = return_follow
    UPLOAD = base + "/upload"
    POST = base + "/post"
    POPULAR = base + "/feed/popular/v2"
    GLOBAL = base + '/feed/global'
    TIMELINE = base + "/timeline"