import webapp2
import re
import urllib2

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

formdata = """
<html>
    <head>
        <title>
            Signup
        </title>
    </head>
    <body>
        <h2>Sign Up</h2>
        <form method="post">
            <label>     Username
                <input type="text" name="username" value="%(user)s"> %(user_error)s
            </label>
            <br>
            <label>     Password
                <input type="password" name="password">%(password_error)s
            </label>
            <br>
            <label>     Verify Password
                <input type="password" name="verify"> %(match_error)s
            </label>
            <br>
            <label>     Email (Optional)
                <input type="text" name="email" value="%(user_email)s"> %(email_error)s
            <label>
            <br>
            <input type="submit">
        </form>
    </body>
</html>
"""

welcome = """
<html>
    <head>
        <title>Welcome</title>
    </head>

    <body>
        <h2>Welcome, %(username)s!</h2>
    </body>
</html>

"""

def valid_user(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    if email:
        return EMAIL_RE.match(email)
    else:
        return True


class MainPage(webapp2.RequestHandler):
    def write_form(self, user="",
                    user_error="",
                    password_error="",
                    match_error="",
                    user_email="",
                    email_error=""
                    ):
        self.response.out.write(formdata % {'user':user,
                                'user_error':user_error,
                                'password_error':password_error,
                                'match_error':match_error,
                                'user_email':user_email,
                                'email_error':email_error,
                                'match_error':match_error})
    def get(self):
        self.write_form()

    def post(self):
        self.response.headers['Content-Type']='text/html'
        uname=self.request.get('username')
        user_password = self.request.get('password')
        verify_password = self.request.get('verify')
        user_mail = self.request.get('email')
        
        user_valid = valid_user(uname)
        password_valid = valid_password(user_password)
        mail_valid = valid_email(user_mail)

        if not user_valid or not user_password:
            self.write_form(user=uname,
                            password_error="That's not valid password",
                            user_error="That's not a valid username",
                            user_email=user_mail,
                            )
        elif not user_valid:
            self.write_form(user=uname,
                            user_error=uname+" That's not a valid username",
                            user_email=user_mail)
        elif not password_valid:
            self.write_form(user=uname,
                            password_error="That's not valid password",
                            user_email=user_mail)
        elif user_password != verify_password:
            self.write_form(user=uname,
                            match_error="Passwords don't match",
                            user_email=user_mail
                            )
        elif not valid_email(user_mail):
            self.write_form(user=uname,
                            user_email=user_mail,
                            email_error="That's not a valid email")
        else:
            self.redirect('/welcome?username='+uname)


class WelcomeHandler(webapp2.RequestHandler):
    def write_form(self,username=""):
        self.response.out.write(welcome%{'username':username})
    def get(self):
        self.write_form(username=self.request.get('username'))


app = webapp2.WSGIApplication([('/',MainPage),
                                ('/welcome',WelcomeHandler)],
                                debug=True
)