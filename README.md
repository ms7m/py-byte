![pybyte-logo](images/logo.svg)

*** 

# Byte API Wrapper for Python
Python 3.6+ Required.
***
**Attention**: This project was built in a weekend (mostly in the weekend that it was launched) as such this is **not production level** software. 

Byte **does not** have an official web API for developers, and most likely this will violate the ToS. Endpoints were found from the mobile app. As such, this wrapper can break at anytime. Do not rely on this wrapper.
***


# Installation
- PyPi (Recommended)
    ```
    pip install pybyte
    ```
- Git repo
    ```
    git clone https://github.com/ms7m/py-byte
    cd py-byte
    python3 setup.py install
    ```
# Usage

```python
>>> import pybyte
>>> byte = pybyte.Byte(TOKEN)
>>> byte.me().username
'cmmvo22123'
>>>
>>> # Set your username/display name/biography
...
>>> byte.me().username = "BotBottyFace220"
>>> byte.me().username
'BotBottyFace220'

>>> # Get Posts
>>> post = byte.get_post("4ZPUKLE5OZB7JJGIBLVMIYQLBU")
>>> post.caption
'@peaks'
>>> post.mentions
[mention1]

# Rebyte/Like posts
>>> post.rebyte()
>>> post.like()

# Comment Posts
>>> post.comment("That's really funny!")


# Upload Posts
>>> byte.upload("sample.mp4", caption="Megan is too funny!")

```



### Example Script

```python
# Check a list of posts, comment and follow the author if they have < 10 followers

posts = [
  'ID1',
  "ID2",
  "ID3"
]

for post in posts:
  	get_post = byte.get_post(post)
    if get_post.author['followerCount'] > 10:
      	get_post.comment("Hey man, thanks for making me laugh!")
        get_post.like()
    else:
      	continue
        
 
```

# Tests
Coming soon
