# -*- coding: utf-8 -*- 
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------


import pandas as pd

from gluon.tools import Mail
mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'nayakpoorna07@gmail.com'
mail.settings.login = 'nayakpoorna07@gmail.com:Project022019'



def error(message="You are not authorized, Please login to continue"):
    session.flash = message
    redirect(URL('index.html'))#add dashboard later


# ---- example index page ----
def index():
    query = ((db.auth_user.id==str(auth.user_id))&(db.auth_user.subject==db.attenmail.subject))
    fields = (db.attenmail.name,db.attenmail.subject,db.attenmail.total,db.attenmail.present,db.attenmail.percentage )
    headers = {'attenmail.name':   'Student Name','attenmail.subject': 'Subject Name','attenmail.total': 'Toatal Days','attenmail.present': 'Present Days','attenmail.percentage': 'Percentage' }
    form = SQLFORM.grid(query=query, csv=True,fields=fields,headers=headers, create=False, details=True, editable=False, deletable=False, paginate=25)
    if not auth.user: response.flash = T("Please Login")
    #if auth.user: 
    return dict(message=T('Welcome to Attendence Tracker Portal !'),form=form)



@auth.requires_login()
def student():
    form = SQLFORM.factory(
           Field('sid',requires = IS_NOT_EMPTY()),
           Field('name',requires = IS_NOT_EMPTY()),
		   Field('subject',db.auth_user)) 
    if form.process().accepted:
       session.sid = form.vars.sid
       session.name = form.vars.name
       session.subject = form.vars.subject
       id = db.student.insert(**db.student._filter_fields(form.vars))
       response.flash = 'Student Details Added !!!'
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form = form)


def upload_attendence():
	import os,csv, subprocess
	files=os.path.isfile("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/upload_attendence.csv")
	if(files):
		for row in db(db.auth_user.id==auth.user_id).select(db.auth_user.subject): #db().select(db.auth_user.subject):
			sub=row.subject

		df=pd.read_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/upload_attendence.csv",)
		df['subject']=sub
		df.to_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/upload_attendence.csv",index=False)
		db.student.import_from_csv_file(open("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/upload_attendence.csv", 'r'))	
		os.remove("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/upload_attendence.csv")
		rows = db(db.student.id>=0).select()
		rows.export_to_csv_file(open("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output_student.csv",'w')	)
		email = db(db.email_data.id>=0).select()
		email.export_to_csv_file(open("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/email_data.csv",'w')	)     
	else:
		response.flash = 'Attendance not taken, please take attendence before uploading. !!!'
	return locals()


def percentile():
    import sqlite3,os
    connection = sqlite3.connect(r"C:\Users\sandeep\Desktop\major project\web2py_win\web2py\applications\gui\databases\storage.sqlite")
    cursor = connection.cursor()
    cursor.execute('delete from percentile')
    cursor.execute('delete from attenmail')
    connection.commit()
    connection.close()
    import pandas as pd
    import numpy as np
    df=pd.read_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output_student.csv")
    df.drop(['student.id'],axis=1, inplace = True) 
    df.columns = ['sid','name','sDate','sTime','subject'] 
    df=df.groupby(["sid","subject"])['sid'].count().to_frame('present')
    df.to_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output.csv")
    df=pd.read_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output.csv")
    array = df.loc[(df['sid']>0)]
    a=df.loc[(df['sid'] == 0)]
    array['total'] = array['subject'].map(a.set_index('subject')['present'])
    array['percentage']=array['subject'].map(a.set_index('subject')['present'])
    array.to_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/total.csv", index=False	)
    df=pd.read_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/total.csv")
    df['percentage']= (df['present']/df['total']*100)
    df.to_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output_percentile.csv",header=True,index=False)
    db.percentile.import_from_csv_file(open("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output_percentile.csv", 'r'))	
    df1=pd.read_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/output_percentile.csv")
    df_per=pd.DataFrame(df1)
    df2=pd.read_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/email_data.csv")
    df2.drop(['email_data.id'],axis=1, inplace = True) 
    df2.columns = ['sid','name','Parent_email'] 
    sid_merge=pd.merge(df1, df2, on='sid', how='right')
    sid_merge.to_csv("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/sid_merge.csv",header=True,index=False)
    db.attenmail.import_from_csv_file(open("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/sid_merge.csv", 'r'))	
    for attenmail in db(db.attenmail).select():
        context = dict(attenmail=attenmail)
        message = response.render('message.html', context)
        x=mail.send(to=[attenmail.Parent_email],subject='Attendance Report of'+'  '+attenmail.subject,message=message)
    if x == True:
      response.flash = 'email sent sucessfully.'
    else:
      response.flash = 'fail to send email sorry!'
    return (dict(attenmail=attenmail),redirect(URL('index.html')))



@auth.requires_login()
def attendence():
    #from sys import executable
    from subprocess import Popen, CREATE_NEW_CONSOLE
    import subprocess
    subprocess.call([r'f.bat'])
    #subprocess.Popen("cmd  final.bat", shell=True)
    #subprocess.Popen("start cmd /k final.bat", shell=True)
    #subprocess.call("start cmd /k f.bat", creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
    return locals(redirect(URL('index.html')))








# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

@auth.requires_login()
def download_percentile():
	rows = db(db.percentile.id>=0).select()
	rows.export_to_csv_file(open("C:/Users/sandeep/Desktop/major project/web2py_win/web2py/applications/gui/private/Attendance/all_student_percentile.csv",'w')	)
	return locals()		
    

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
