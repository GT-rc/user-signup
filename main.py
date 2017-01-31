#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

#html boilerplate for the top of the page
header = '''
    <!DOCTYPE html>
    <html lang='en'>
        <head>
            <meta charset="utf-8">
            <link type="text/css" rel="stylesheet" href="stylesheet.css" />
            <title>User Signup</title>
        </head>
        <body>
            <h1><a href="/">User Signup</a></h1>
'''

#html boilerplate for the bottom of the page
footer = '''
        </body>
    </html>
'''

#form data
form_main = '''
    <form method="post">
        <table>
        <tbody>
            <tr>
                <td><label>Username:</label></td>
                <td><input type="text" name="username"  pattern="^[a-zA-Z0-9_-]{3,20}$" value="" required />

                </td>
            </tr>
            <tr>
                <td><label>Password:</label></td>
                <td><input type="password" name="password" pattern="^.{3,20}$" required />

                </td>
            </tr>
            <tr>
                <td><label>Confirm Password:</label></td>
                <td><input type="password" name="password2" required />

            </tr>
            <tr>
                <td><label>Email: (optional)</label></td>
                <td><input type="email" name="email" value="" />

            </tr>
        </tbody>
        </table>
        <br>
        <input type="submit" />
    </form>
'''


class MainHandler(webapp2.RequestHandler):
    def verify_username(self, username):
        un = self.request.get("username")
        temp = re.compile("^[a-zA-Z0-9_-]{3,20}$")
        username = temp.match(un)
        if username == True:
            return True
        else:
            return False

    def verify_password(self, password):
        pw = self.request.get("password")
        temp = re.compile("^.{3,20}$")
        password = temp.match(pw)
        if password == True:
            return True
        else:
            return False

    def valid_email(self, email):
        em = self.request.get("email")
        temp = re.compile("^[\S]+@[\S]+.[\S]+$")
        email = temp.match(em)
        if email == True:
            return True
        else:
            return False

    # def create_form(self, username="", email=""):
    #     self.response.write(form_main % {"username": username, "email": email})

    def get(self):
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""
        #form = self.create_form()
        self.response.write(header + form_main + error_element + footer)

    def post(self):
        username = self.request.get("username")
        pass1 = self.request.get("password")
        pass2 = self.request.get("password2")
        email = self.request.get("email")

        if not username or (self.verify_username(username) == False):
            error = "Please enter a valid username."
            self.redirect('/?error=' + error)

        if (pass1 != pass2) or (pass1 == '') or (pass2 == ''):
            error = "Your passwords do not match. Please enter matching passwords."
            self.redirect('/?error=' + error)

        if pass1 == '' and pass2 == '':
            error = "Please enter a valid password."
            self.redirect('/?error=' + error)

        if email and self.valid_email(email) == False:
            error = "Please enter a valid email."
            self.redirect('/?error=' + error)

        #form = self.create_form(username, email)
        content = header + form_main + footer
        self.response.write(content)


class ThankYouHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        self.response.write("<h2>Welcome, " + username + "!</h2>")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thankyou', ThankYouHandler)
], debug=True)
