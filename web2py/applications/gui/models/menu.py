# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#################### #####################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Attendence Tracker'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://127.0.0.1:8000/gui/default/index")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Poornachandra M <poornachandra7897@gmail.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################


response.menu = [ (T('Home'), False, URL('default', 'index'), []),
                  (T('Upload Attendence'), False, URL('default', 'upload_attendence'), []) ,
                  (T('Take Attendence'), False, URL('default', 'attendence'), []),
                  (T('Take  Percentile'), False, URL('default', 'percentile'), []),
				  (T('Download  Percentile'), False, URL('default', 'download_percentile'), [])               
                ]

if "auth" in locals(): auth.wikimenu()
