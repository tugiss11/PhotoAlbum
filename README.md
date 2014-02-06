group-7-2013
============

Final Submission
----------------
Features By Creator

Joona Heinikoski 79655J
- Database
    - Works well and reliably
    -
    -


Liang

Tuukka


Planning
--------

Introduction
------------

Our plan is to implement as many of the proposed features as we can in the given time. First we are going to make the basic functionalities and authentication to work. This should take about 2 weeks to complete. After that we will split the extra features between the team members and try to implement one feature a week. We are planning to meet once a week and do most of the development on our own time. We will start working a bit after new year.

Basic functionalities
---------------------

Our plan is to keep the system simple, while still providing good functionality. This means we will have only quite few views and database models. Our views will include a login view, list of albums view, album edit view and album view. These view should allow us to implement all the features. Our plan is to minimize the amount of completely new page loads as the user makes changes to the album, they will be updated dynamically using AJAX. In the list of albums view the user will be able to add and remove albums.

![alt text](http://i.imgur.com/TueWnlD.png)

Rudimentary idea of the album list page


The user will be able to choose a premade layout for every album page. These pages will follow a standardized structure and the actual layout is defined in css. Practically there will probably be container div-elements for pictures with id’s such as “img1”, “img2” and so forth. In the album edit view user will be able to add and remove pages, change page layout and set the link and caption for images. Album editing will be communicated to server with http POST requests that contain information on what was edited.

![alt text](http://i.imgur.com/my6xC95.png)

Album editing page

The database will keep information about users and albums. For users, we are going to mainly use Django’s standard User model. For albums, we will actually need three models; Album, Page and Image. Albums will have information if it’s owner, public link, how many times it has been opened and list of its pages. We are also thinking of allowing users to like and dislike albums and also these counts will be saved in Album model. The Page model will have information of what Album it belongs to, what layout it has and list of its Images. The Image objects will only have information on what page it belongs to, the link and caption.

Authentication
--------------

Our plan is to use the user authentication system provided by Django. Django auth system makes it possible to set different permissions to logged in users and other users. Users objects have attributes of username, password and email.  Django framework does not store raw password but only a hash. Authentication is performed with the username and password. Logging in saves the user’s id in the session with Django’s session framework. Logging out clears the session data for the current user. Other users have limited access that means they do not have all the same functionalities as logged in users. Possible other functions of auth system are changing or resetting a password. User email can be used for resetting the password.



Public link to photo albums
---------------------------

Users have possibility to link their albums to their friends. Preventing people from guessing the album ids and traversing through them all, we plan to generate external ids that are random 8 character fields. The resulting link would then be, for example HOST/show_album?id=k8h6uu9lo. These ids are stored in the database. It is secure to share these links, because the page will always check if the user is authenticated or not and then user has access on functionalities based on that. Other alternative could be having dynamic links that hide the real path to the album and unauthorized users could access albums only through that way but we think it is not necessary to have an approach like that.

Ordering albums
---------------

We also plan to implement the ordering function, but it has lower priority than other functions. Ordering function makes it possible for user to place an order for printed album and then pay the order. Payment requests would be sent to external service provided by our university that simulates payments. Basically, ordering an album will send a HTTP POST request to payment service. Orders need attributes that are order id, seller id, amount of payment, resulting url and checksum. There are three resulting urls that are called in three different cases. In the case one, user made a successful payment, in the case two, a payment failed, and in the third case, user cancelled a payment. Seller id is used to generate a secret key for the payment service. Secret key is then used with the payment id, amount and seller id to calculate an MD5-hash of the checksum. The payment is successful when the checksums match.

3rd party login
---------------

The service will allow user to login with Facebook. Facebook provides OAuth authentication method for web services. We could write our own system to handle the authentication process, but it is somewhat complicated. Instead we will use “django-all-access” application for implementing this feature. All-access provides generic support for OAuth 1 and 2, but we are going to only use it for Facebook. Adding the support for Facebook login using all-access should be quite straightforward as All-acces uses Django’s standard User objects. After logging in with All-acces, handling the user’s status shouldn’t differ from using the default username + password login method.

Django-all-access can be downloaded from https://github.com/mlavin/django-all-accesss. 

Share albums
------------

In order to keep the homepage clear, so we planed to add the share button to the picture page, the visitor could justclick the demand share logo of specifical site then the page will redirect to the related site and the vistor could also add some description of their own and then share to their friends, the share button will at least include Facebook, twitter, using the related site’s share code. The share button will add to the picture page. As for the share ways, the above way is the basic way to share picture and we try to add some more share ways to share picture, and we try to add some more share ways like URL sharing. We will consider the album share as the development of the layout of this site.

Integrate with an image service API
-----------------------------------

We want get to the pictures from Flickr (http://www.flickr.com/services/api/) and display them outside of Flickr, so we will through the Flickr API, the images will show up in API requests, also in order to display the pictures what we want, we will get dynamic content and display photos via tags or user ID or other interesting ways.

Use of Ajax and dynamic UI
--------------------------

The most usage of Ajax is like change album pages or remove the dislike album without refresh the page, meanwhile, we will add the like/dislike function button, meanwhile, we could also zoom in the pictures in the album also without opening a new page and the visitor could just click left or right arrows to change the pictures and click the closed sign to close the picture. Last, in order to enhance the personalization we will try to add the function that will allow the visitors to drag the thumb of the album and make the sequences in their own ways
