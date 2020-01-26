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

# Features
- View Byte Profile ``ByteUser, ByteAccount``
- View Byte Posts: ``BytePost``
- Send authenticated requests to Byte API ``ByteSession``
- Check for usernames

# To Do
- Update user information 
- Interact with posts 
- Change Username
- Follow users
- Rebyte Posts

# Usage

```python
>> import pybyte

>> byte = pybyte.Byte(<google auth token>)
>>> me = byte.me()
>>> me
<pybyte.user.ByteAccount object at 0x1069a2150>

...

>>> me.user().user_id
'MZBW6JBYUBDKBMQK62LCBS7I6Q'
>>> me.user().username
'gjoder'
>>> me.user().registered
datetime.datetime(2020, 1, 26, 4, 40, 57, tzinfo=tzutc())
>>> 

```

**Attention**: You'll only need to supply a google OAuth (Soon to be done automatically) *once* and pybyte will cache the authorization token for you. After doing this one time, simply call ``pybyte.Byte`` without any arugments.

# Tests
Coming soon