

base = "https://api.byte.co"
def return_like(string)
    return base + f"/post/id/{string}/feedback/like"

class Endpoints:
    GOOGLE_LOGIN = base + "/authenticate/google"
    ACCOUNT = base + "/account/me"
    USERNAME_CHECK = base + "/"
    OTHER_ACCOUNT = base + "/account/id/"
    POST_INFO = base + "/post/id/"
    REBYTE = base + "/rebyte"

    

    LIKE = return_like