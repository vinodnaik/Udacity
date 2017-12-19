import webapp2
import cgi
import string

formdata = """
<form method="post" >
    <label>Enter your text here<br>
        <textarea name="text" rows="10" cols="50">%(text)s</textarea>
    </label>
    <br><br>
    <input type="submit">
</form>
"""
alpha_lower = string.lowercase
alpha_upper = string.uppercase
lower_dict = dict((alpha_lower[m],alpha_lower[(m+13)%26]) for m in range(0,26))
upper_dict = dict((alpha_upper[m],alpha_upper[(m+13)%26]) for m in range(0,26))
rot_dict = lower_dict.copy()
rot_dict.update(upper_dict)

def Rot13(s):
    return "".join([rot_dict[m] if m in rot_dict.keys() else cgi.escape(m, quote=True) for m in s])

class MainPage(webapp2.RequestHandler):
    def writeform(self,text=""):
        self.response.out.write(formdata%{"text":text})

    def get(self):
        self.response.headers['content-type']='text/html'
        self.writeform()

    def post(self):
        user_text =self.request.get('text')
        self.writeform(Rot13(user_text))

app = webapp2.WSGIApplication([('/',MainPage),],debug=True)