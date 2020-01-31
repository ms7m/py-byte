![pybyte-logo](images/logo.svg)

*** 

# A Python wrapper for the byte.co app.
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
>>> 
>>> byte = pybyte.Byte("7WMRREHUQRH4DBK7DQCV7YWL44")
>>> 
>>> byte.me().username
'BotBottyFace220'
>>> 
>>> my_timeline = byte.me().timeline()
>>> 
>>> # no rate limit protection yet. do it at your own risk!
... 
>>> import time
>>> 
>>> for post in my_timeline.feed:
...     print(f"Caption: {post.caption}")
...     time.sleep(1)
...     print(f"Author: {post.author.username}")
...     print('\n')
... 
Caption: 
Author: BotMcBotFace2300


Caption: Nice
Author: BotMcBotFace2300


Caption: 
Author: BotMcBotFace2300


Caption: 
Author: BotMcBotFace2300


Caption: @peaks 
Author: BotMcBotFace2300
# ...
>>> 
>>> 
>>> # Set your own username
... 
>>> byte.me().username = "BotMcBotFace2300"
>>> byte.me().username
'BotMcBotFace2300'
>>> 
>>> # Get Posts
... 
>>> post = byte.get_post("4ZPUKLE5OZB7JJGIBLVMIYQLBU")
>>> post.caption
'@peaks '
>>> post.mentions
[<pybyte.user.ByteUser object at 0x10b33b550>]
>>> 
>>> # rebyte / like posts
... 
>>> post.rebyte()
True
>>> post.like()
True
>>> 
>>> # comment posts
... 
>>> post.comment("Haha!")
True
>>> 
>>> # Upload Posts
... 
>> byte.upload('sample.mp4', caption="haha too funny!")
>> # Automatically generate a thumbnail
>> byte.upload('sample.mp4', caption="haha too funny!", generate_thumbnail=True)
>> # Supply your own thumbnail!
>> byte.upload('sample.mp4', caption="haha too funny", providedThumbnail="ultraCoolthumbnail.jpg")

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
