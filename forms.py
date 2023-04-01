from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, SelectMultipleField, StringField, TextAreaField,HiddenField,IntegerField,FileField
from wtforms.validators import InputRequired, Length, ValidationError
from models import Tag

class LoginForm(FlaskForm):  

    username = StringField(validators = [InputRequired()])

    password = PasswordField(validators = [InputRequired(),Length(min=4,max=20)])

    submit = SubmitField("Login")

class SignupForm(FlaskForm):

    username = StringField(validators = [InputRequired()])

    password = PasswordField(validators = [InputRequired(),Length(min=4,max=20)])

    submit = SubmitField("Signup")

class PostForm(FlaskForm):

    title = StringField('Title', validators=[InputRequired()])

    Post = TextAreaField(validators=[InputRequired])

    tags = SelectMultipleField('Tags')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Populate the tags field with all existing tags
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]