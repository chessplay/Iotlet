# -*- coding:utf-8 -*-
from flask_wtf import Form,FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,SelectField,RadioField,SelectMultipleField
from wtforms.validators import Required,DataRequired,Length,Email,EqualTo,ValidationError
from models import User

class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()],render_kw={'class':'weui-input'})
    password=PasswordField("password",validators=[DataRequired()],render_kw={'class':'weui-input'})
    remember_me=BooleanField('Remember Me')
    submit=SubmitField(u'登入',render_kw={'class':'weui-btn weui-btn_plain_primary'})
class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()],render_kw={'class':'weui-input'})
    email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'class':'weui-input'})
    password=PasswordField('Password',validators=[DataRequired()],render_kw={'class':'weui-input'})
    password2=PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')],render_kw={'class':'weui-input'})
    submit=SubmitField(u'注册',render_kw={'class':'weui-btn weui-btn_plain_primary'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
class SettingForm(FlaskForm):
    appname=StringField('appname',validators=[DataRequired()],render_kw={'class':'weui-input'})
    serveraddr=StringField('serveraddr',validators=[DataRequired()],render_kw={'class':'weui-input'})
    rtmpaddr=StringField('rtmpaddr',validators=[DataRequired()],render_kw={'class':'weui-input'})
    controller=SelectField('controller',choices=[
        ('80C51', '80C51'),
        ('STM32', 'STM32')
    ],validators=[DataRequired()],render_kw={'class':'weui-select'})
    module=SelectField('module',choices=[
        ('LED', 'LED'),
        ('Camera', 'Camera')
    ],validators=[DataRequired()],render_kw={'class':'weui-select'},)
    submit=SubmitField(u'设置',render_kw={'class':'weui-btn weui-btn_primary'})
