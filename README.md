group-7-2013
============

Final Submission
----------------
Memory Album can be found from http://memory-album.herokuapp.com/
Usage should be pretty straigth-forward and self-explanitary. Not logged in users will see latest public albums in main view. User can log in or create account from top-right button. Logged in users will see buttons for editing albums in top of the page. Tools near albums and images edit corresponding item. When viewing album, logged in users can hide edit tools by unchecking "Edit mode" checkbox from top of the page. Album can be made public by checking "Public" checkbox and shared to Facebook by clicking on Share button. Public album urls can be copied from browser location bar and shared. User can either enter URL where to fetch the images from or search from Flickr.

Following features were implemented. We give points for features in brackets. Features are discussed more in depth by team member who mainly implement them.
- Authentication (200 / 200)
- Basic album functionalities (450 / 500)
- Public link to photo albums (70 / 70)
- Share albums (70 / 80)
- Order albums (150 / 200)
- Integrate with an image service API (80 / 100)
- Use of Ajax (80 / 100)

Not implemented:
- Third party login
    - We wanted to polish other features and improve reliability

Features By Creator
-------------------
Joona Heinikoski 79655J
- Backend developer
- Album functionality (Basic functionality)
    - All requested features are implemented
    - All modifications are sent to /modify with a CSRF protected and enforced POST request
- Database (Basic functionality)
    - Works well and reliably
    - Relations between meaningful objects and unique id's (uuid4) to identify everything
    - Helper functions for creating new Albums and Pages
    - Reliable deletion (All associated objects are deleted)
    - Function to fix possible problems in page indexing
- Album ownership (Authentication)
    - Only owner can edit their albums
    - Albums are by default not visible to anyone else, single click to make public
    - All modifications are owner-checked
- Public link to photo albums
    - Album's unique id is used for creating link (example /album/c1bc861f-0dfc-45fd-9560-d6fcc79e8889)
    - Same link for editing and viewing album
    - If album is public but current user is not the owner of album, albun can be viewed but not edited
    - Album page can be part of link
- Share albums
    - Users can click one button to share album on Facebook
    - Default Facebook share button used
- Order albums
    - User can click to order album
    - No choises for different types of books/multiple copies
    - Basic info from user, name, address, e-mail
    - After info is provided, order is saved to database and can be paid or cancelled
    - A view to see all user's orders and pay/cancel non-paid orders
- Integrate with an image service API
    - User can search for images from Flickr
    - Random matching results shown, choose image with one click
    - Shown Images are from 50000 most relevant images
    - Simple error page in case of problems (Flickr was down once during development)
- Making albums public (AJAX)
    - Checking/Unchecking "Public" checkbox sends AJAX request to change public status of album
- Edit mode (Dynamic UI)
    - Album editing tools can be hidden and shown by Checking/Unchecking "Edit mode" checkbox

Liang GUO 397616
- User interface developer
- Index View
    - Come up with the Name called "MemoryAlbum" and first designed the index page which I wnat to emphesisze the LOGO and give the first strong impression to the visitor.
- Login and Register View
    - Check the username is taken or not then give the feedback to the user.(Ajax)
    - Designed the Login and Register page and focus on the key point, I don't want to bother the visitor in this step, so keep the process as simple as possible.
- The album list View
    - Use the new feature of CSS3 "Multi-Column Layout properties" to create multi-column grid layouts with an automatic content spill over feature.
    - Designed the default "Memory Album" picture using photoshop.
    - If the album was new created and there was no picture then the thumbnail will be shown as the "Memory Album" default picture automatically. And when the user linked picture then the album thumbnail will change.
    - Add the "Add Album"/"My order" buttons.
    - Layout the Album to show the "title","caption","Order" and "Remove", also layout the bottom information bar.
- The Album Page View
    - I designed several different kinds of layouts which the user could choose what they like. The new album has the "default layout", other layouts are in different shapes or differnt numbers or shapes.
    - The page layout Also use the "Multi-Column Layout properties".
    - Made the bottom jump page bar using javascript which user could visit the next/previous or customize page.
    - Made the Dropdown Setting button and add the "Add page", "Remove Page" and "Change Layout" button in it.
    - When the user Remove Page, I made a warning popup page to let the users ensure their action. 
- The filckr search page View
    - Made 5 column "multi-column" layout which the page could load more pictures at one time.
- The Order Album Page
    - Made the order album page and let the user to ensure the information before payment.
- All the template html files and CSS files are validated by W3C except these file:
    - invalid.html (because Tuukka use extend tag)
    - logout.html  (the same reason)
    - newuser.html (the same reason)
    - bootstrap.css (I did my css with the aid of bootstrap I didn't change it any more, but it could not be validated by W3C)


Tuukka Järvinen 79439A

- Authentication
    - Uses Django auth
    - Logging in/out and creating accounts works fine

- Album functionality (Basic functionality)
    - User can write album descriptions
    - User can set captions for images

- Usability improvements
    - Language
    - Navigation
    - Differences between authenticated and non-authenticated views
    


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
