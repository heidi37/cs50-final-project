# Let's Do Brunch - CS50 Final Project

<img src="/static/images/screenshot.png" alt="screenshot of my CS50 Brunch App" />

## Video Demo

https://youtu.be/zXS2b5kVV1w

## Description

This is a web application that allows you to create a brunch event at a specific date, time and location. You may then add guests and what they are bringing to the newly created brunch. There is a feature to copy the URL of the brunch guest list and send to someone so they may add themselves and their dish to the guest list.

Only brunches that are in the future will display on the guest list.

The guest list displays the percentages of the types of dishes the guests are bringing based on these four types of dishes: Carbohydrate, Fruit, Beverage or Protein. In theory if there are a lot of items in one category, the guest will likely choose another type of dish when faced with these percentage figures. The figures turn red when exceeding 25% for a dish type.

Functionality is built in to delete a brunch that will delete all the related guests as well. Also the abilty to delete just one guest from a brunch list is available.

**Backend:** The application is built with Python for logic. SQL is used for querying and modifying the database. Flask is what converts the templates to HTML utilzing the Jinga templating language.

**Frontend** The front end is HTML, CSS utilzing the Bootstrap framework, and there is a javascript feature that copies the URL of the current brunch list so that you can share it with others and they can add themselves to the guest list.

**layout.html** - template for providing HTML elements that display on all page

**index.html** - template for the home page, just text, not dynamic

**create-brunch.html** - form to create a new brunch, redirects to **brunch-list.html**

**brunch-list.html** - pulls in **brunch-table.html** to dynamically display a list of brunches with a start date greater than or equal to today

**add-guest.html** - form to add a guest to a brunch, redirects to display **guest-list.html** for the current brunch

**guest-list.html** - displays the guest list based on the id of the brunch that is passed to it **app.py**. It pulls in dynamically the **dishes-table**.

**guest-deleted.html** - when a guest is deleted, redirects to a guest page without the last deleted guest and shows a message confirming the guest is deleted

**success.html** - displays when a guest is successfully added, added this functionality to prevent duplicates on refreshing the page after adding a guest.

**failure.html** - displays if server side validation fails

**app.py** - contains all python code, utlized flask for for dynamic HTML templating, sqlite for querying the database

**/static/app.js** - a javascript function to copy the URL of a brunch to the clipboard so it can be shared

**/static/styles.css** - External CSS stylesheet, also utilzied Bootstrap for styling from a CDN

[View Live Project](https://heidi37.pythonanywhere.com/)
