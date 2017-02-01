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
                <td><input type="text" name="username"   value="%(username)s" required /></td>
                <td><p>%(error_un)s</p></td>
            </tr>
            <tr>
                <td><label>Password:</label></td>
                <td><input type="password" name="password"  value="" required /></td>
                <td><p>%(error_password)s</p></td>
            </tr>
            <tr>
                <td><label>Confirm Password:</label></td>
                <td><input type="password" name="password2" value="" required /></td>
                <td><p>%(error_verify)s</p></td>
            </tr>
            <tr>
                <td><label>Email: (optional)</label></td>
                <td><input type="email" name="email" value="%(email)s" /></td>
                <td><p>%(error_email)s</p></td>
            </tr>
        </tbody>
        </table>
        <br>
        <input type="submit" />
    </form>
'''

def escape_html(s):
    return cgi.escape(s, quote=True)


class MainHandler(webapp2.RequestHandler):
    def verify_username(self, username):
        un = self.request.get("username")
        temp = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        username = temp.match(un)
        if username == True:
            return True
        elif username == None:
            return False

    def verify_password(self, password):
        pw = self.request.get("password")
        tempa = re.compile(r"^.{3,20}$")
        password = tempa.match(pw)
        if password == True:
            return True
        elif password == None:
            return False


    def valid_email(self, email):
        EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return not email or EMAIL_RE.match(email)


    def create_form(self, username="", email="", error_un="", error_password="", error_verify="", error_email=""):
        return (form_main % {"username": username,
                            "email": email,
                            "error_un": error_un,
                            "error_password": error_password,
                            "error_verify": error_verify,
                            "error_email": error_email
                            })

    def get(self):

        form = self.create_form()
        self.response.write(header + form + footer)

    def post(self):
        username = self.request.get("username")
        pass1 = self.request.get("password")
        pass2 = self.request.get("password2")
        email = self.request.get("email")
        has_error = False

        parameters = dict(username=username, email=email)

        if not username or (self.verify_username(username) == False):
            has_error = True
            parameters['error_un'] = "Please enter a valid username."
            #self.redirect('/?error_un=' + error_un)

        if pass1 == '' and pass2 == '':
            has_error = True
            parameters['error_password'] = "Please enter a valid password."
            #self.redirect('/?error_password=' + error_password)

        if (pass1 != pass2) or (pass1 == '') or (pass2 == ''):
            has_error = True
            parameters['error_verify'] = "Your passwords do not match. Please enter matching passwords."
            #self.redirect('/?error_verify=' + error_verify)

        if not self.valid_email(email):
            has_error = True
            parameters['error_email'] = "Please enter a valid email."
            #self.redirect('/?error_email=' + error_email)

        if has_error == False:
            self.redirect('/thankyou?username=' + username)


        form = self.create_form(**parameters)

        self.response.write(header + form +footer)


class ThankYouHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write(header + "<h2>Welcome, " + username + "!</h2>" + footer)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thankyou', ThankYouHandler)
], debug=True)
