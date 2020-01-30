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

>>> # View your timeline
>>> my_timeline = byte.me().timeline()
>>> # iterate over your timeline feed
>>> for post in my_timeline.feed:
>>>     print(post.caption)
>>>     print(post.author)
>>>     post.comment("Hey!")



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
# Go through the global feed, comment and follow the author if they have < 10 followers

global_feed = byte.me().global_feed()

for post in global_feed.feed:
    if post.author.followers['followerCount'] > 10:
      	post.comment("Hey man, thanks for making me laugh!")
        post.like()
    else:
      	continue
        
 
```

### Example Scripts

```python
# Go through your posts and comment any post older than 3 days and has less than 200 likes

my_posts = byte.me().posts()
time_now = datetime.datetime.now()

for post in my_posts.feed:
    if (time_now - post.date).days > 3:
        if post.like_count < 200:
            # i am not popular :(
            post.comment("this post isn't making me popular")
         else:
            post.comment("Woohoo! I'm very popular!")
    else:
        # not old enough
        continue
```

# Tests
Coming soon
