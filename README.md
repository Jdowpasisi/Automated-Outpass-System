CONTENTS

Slide 1: Why we need automated system
Slide 2: Principle of operation
Slide 3: Working
Slide 4: Advantages

STRUCTURE:
•	app.py: holds python based flask code that serves as an entry point to the application.
•	templates: 
◦	index.html/base.html: home page of the website. Includes links: sign-up, login (required), abort, outpass, layout, etc.
◦	sign_up.html: once signed up, it will redirect to login page.
◦	login.html: once logged in, it will direct to have home page.
◦	outpass.html: contains the form same as outpass form. Once submitted it will redirect to home page (only one form can be submitted at one time). 
◦	admin.html: will show the admin the list of forms of the students (to accept, to reject)

•	status: styling content 
◦	css 
◦	images

Once the admin approves, an email will be sent to the registered email.
