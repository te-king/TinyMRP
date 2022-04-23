from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, BooleanField, SelectField,\
    SubmitField, DateField, FieldList,FormField,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from .models import Part, Job, mongoJob, mongoPart, mongoOrder, mongoSupplier



#Testing flask WTF to make forms easier
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField,SelectField,TextAreaField, RadioField
from wtforms.validators import DataRequired

from datetime import datetime, date



from pymongo import MongoClient

client = MongoClient("localhost", 27017)
mongodb=client.TinyMRP
partcol=mongodb["part"]
jobcol=mongodb["job"]
ordercol=mongodb["order"]
suppliercol=mongodb["supplier"]


#bring configset
from config import config as config_set
config=config_set['tinymrp'].__dict__
allprocesses=list(config['PROCESS_CONF'].keys())
availableprocesses=[("","")]+[(x,x) for x in allprocesses]
availableprocesses.sort()




class CreateOrder(FlaskForm):
    ordernumber = StringField("order Number", validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'order numbers must have only letters, numbers, dots or '
               'underscores')])
    description = StringField("Description")
    supplier =StringField("Supplier")
    job= SelectField('Job Number')
    
    submit = SubmitField('Create order')
  

    def validate_ordernumber(self, field):
        if mongoOrder.objects(ordernumber=field.data):
                raise ValidationError('ordernumber already in use.')




class CreateJob(FlaskForm):
    jobnumber = StringField("Job Number", validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Job numbers must have only letters, numbers, dots or '
               'underscores')])
    description = StringField("Description")
    customer =StringField("Customer")
    
    
    submit = SubmitField('Create Job')

    def validate_jobnumber(self, field):
        if mongoJob.objects(jobnumber=field.data):
                raise ValidationError('Jobnumber already in use.')


class CreateSupplier(FlaskForm):


    suppliername = StringField("Supplier name", validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Job numbers must have only letters, numbers, dots or '
               'underscores')])
    description = StringField("Description")
    address =StringField("address")
    location =StringField("location")
    contact =StringField("contact")
    processes= FieldList( SelectField('Process', choices=availableprocesses), min_entries=5, max_entries=5)
    submit = SubmitField('Create Supplier')

    def validate_suppliername(self, field):
        if mongoSupplier.objects(suppliername=field.data):
                raise ValidationError('suppliername already in use.')




class UploadForm(FlaskForm):
    file = FileField('Attach file',validators=[FileRequired()])
    submit = SubmitField('Submit')


class PartComment(FlaskForm):
    body = TextAreaField('Add a comment', validators=[DataRequired()])
    category=RadioField('Comment type', validators=[DataRequired()],choices=[('review','Design review'),('improvement','improvement'),('mistake','mistake'),('procurement','procurement'),('ideas','ideas')])
    pic_path = FileField('Attach file',validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')


class PartReport(FlaskForm):
    body = TextAreaField('Add a comment', validators=[DataRequired()])
    category=RadioField('Comment type',choices=[('improvement','improvement'),('mistake','mistake'),('procurement','procurement')])
    pic_path = FileField('Attach file',validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')    
