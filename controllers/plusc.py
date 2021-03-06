from twilio import twiml
from twilio.rest import TwilioRestClient

# coding: utf8

'''
Use Cases:
- Add location with contact info, SMS number
- Send message to location (status = 'processed')
- Receive message from location (status - 'received')
- Edit message (e.g., mark as accepted, processed)
- Manage list of locations (with links to edit, send message, etc.)
- Manage list of messages (e.g., view new messages)
'''

# smartgrid defaults
defExportClasses = dict(csv_with_hidden_cols=True, csv=True, xml=False, html=False, tsv_with_hidden_cols=False, tsv=False)
defShowbuttontext = True

# SMS Phone Numbers
# 'some number' # PLUS Portal Twilio Gateway
# 'some number' # Laundrylux Test Gateway
# 'some number' # Person Cell

@auth.requires_login()
def send_message():
    db.t_plus_sms_message.f_from.default = '"some number"' # PLUS Portal Twilio Gateway
    db.t_plus_sms_message.f_from.writable = False
    db.t_plus_sms_message.f_location.default = 0
    db.t_plus_sms_message.f_status.default = 'Processed'
    db.t_plus_sms_message.f_direction.default = 'Sent'
    
    form=SQLFORM(db.t_plus_sms_message, fields=['f_location', 'f_body'])
    
    # TODO selecting locationnumber should be performed after the form is accepted and remove the 'to' phone number from the sms_message table
    if request.vars.f_location:
        locationNumber = db(db.t_plus_location.id==request.vars.f_location).select().first().f_sms_phone_number
        db.t_plus_sms_message.f_to.default = locationNumber

    if form.process().accepted:
        session.flash = 'form accepted'
        
        # test credentials
        # twilioAccount = "account number"
        # twilioToken = "token number"
        # twilioFrom = 'some number' # for successful sms send
        
        # live credentials
        twilioAccount = "account number"
        twilioToken = "account token"
        twilioFrom = 'from number'
        
        client = TwilioRestClient(twilioAccount, twilioToken)
        message = client.sms.messages.create(to=locationNumber, from_="some number, body=form.vars.f_body)
                                 
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill the form'
    return dict(form=form)
    
def send_points():
    db.t_plus_sms_message.f_from.default = '"some number"' # PLUS Portal Twilio Gateway
    db.t_plus_sms_message.f_from.writable = False
    db.t_plus_sms_message.f_location.default = 0
    db.t_plus_sms_message.f_status.default = 'Processed'
    db.t_plus_sms_message.f_direction.default = 'Sent'
    
    form=SQLFORM(db.t_plus_sms_message, fields=['f_location', 'f_points', 'f_sales_order_num'])
    
    # TODO selecting locationnumber should be performed after the form is accepted and remove the 'to' phone number from the sms_message table
    if request.vars.f_location:
        locationNumber = db(db.t_plus_location.id==request.vars.f_location).select().first().f_sms_phone_number
        db.t_plus_sms_message.f_to.default = locationNumber
        sms_body = db.t_plus_sms_message.f_body.default = "Service 0 32 %s" % request.vars.f_points

    if form.process().accepted:
        session.flash = 'form accepted'
        send_sms(locationNumber, sms_body)
                                 
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill the form'
    
    return dict(form=form)

def send_points2():
    db.t_plus_sms_message.f_from.default = 'some number' # PLUS Portal Twilio Gateway
    db.t_plus_sms_message.f_from.writable = False
    db.t_plus_sms_message.f_location.default = request.vars.locid
    #db.t_plus_sms_message.f_location.writable = False
    db.t_plus_sms_message.f_points.default = request.vars.points
    #db.t_plus_sms_message.f_points.writable = False
    db.t_plus_sms_message.f_status.default = 'Processed'
    db.t_plus_sms_message.f_direction.default = 'Sent'
    db.t_plus_sms_message.f_parent_msg.default = request.vars.smsmsgid
    
    form=SQLFORM(db.t_plus_sms_message, fields=['f_location', 'f_points', 'f_sales_order_num'])
    
    # TODO selecting locationnumber should be performed after the form is accepted and remove the 'to' phone number from the sms_message table
    if request.vars.f_location:
        locationNumber = db(db.t_plus_location.id==request.vars.f_location).select().first().f_sms_phone_number
        db.t_plus_sms_message.f_to.default = locationNumber
        sms_body = db.t_plus_sms_message.f_body.default = "Service 0 32 %s" % request.vars.f_points

    if form.process().accepted:
        session.flash = 'form accepted'
        send_sms(locationNumber, sms_body)
        
        # update sms alert
        row = db(db.t_plus_sms_message.id==request.vars.smsmsgid).select().first()
        row.update_record(f_status='Processed')
        
        redirect(URL('manage_alert_msgs'))
                                 
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill the form'
    
    #request.function = 'Send %s Points to %s' % (request.vars.points, request.vars.locid)
    request.function = 'Send Points'
    
    return dict(form=form)
    
def send_sms(sms_to, sms_body):
    # test credentials
    # twilioAccount = "account number"
    # twilioToken = "token number"
    # twilioFrom = 'some number' # for successful sms send
    
    # live credentials
    twilioAccount = "account number"
    twilioToken = "token number"
    twilioFrom = 'some number'
    
    client = TwilioRestClient(twilioAccount, twilioToken)
    message = client.sms.messages.create(to=sms_to, from_="some number", body=sms_body)
    
    return message
    
def send_email(email_to, email_subject, email_body):
    
    # email_to = ["some email"]
    mail.send(to = email_to, subject = email_subject, reply_to = 'PLUS Portal', message = email_body)

def emailtest():
    
    email_to = ["some email"]
    mail.send(to = email_to, subject = "PLUS Alert - 1 Week Alert", reply_to = 'PLUS Portal', message = 'just for fun')

def receivesms():
    ''' receive sms message, insert into db, reply for confirmation '''
    # test with /plusc/receivesms?From=somenumber&To=somenumber&Body=Hello

    sender_number = request.vars['From'][-11:]
    location = db(db.t_plus_location.f_sms_phone_number==sender_number).select().first()
    if location:
        location_name = location.f_name
        location_four_week_point_level = location.f_four_week_point_level
    else:
        location_name = sender_number
        location_four_week_point_level = "unknown"
            
    sms_message_id = db.t_plus_sms_message.insert(
        f_from = request.vars['From'],
        f_location = location.id,
        f_to = request.vars.To,
        f_body = request.vars.Body,
        f_status = 'New',
        f_direction = 'Received')
        
    db.commit()
        
    #sender = request.vars['From'][-10:]+'@vtext.com'
    #mail.send([sender],'hello',request.vars.Body)
    
    # for testing ...
    if location.id == 5:
        alert_to_1_week_email = alert_to_2_week_email = ['some email']
    else:
        alert_to_2_week_email = ['some email', "another email"]
        alert_to_1_week_email = ['some email', "another email"]

    send_loc_points_url = URL('send_points2', vars=dict(locid=location.id, smsmsgid=sms_message_id, points=location_four_week_point_level), scheme=True, host=True)
    
    context = dict(location=location_name, send_loc_points_url=send_loc_points_url, msg=request.vars.Body, four_week_point_level=location_four_week_point_level, sms_message_id=sms_message_id)
    alert_body = response.render('plusc/notify.html', context)


    alert_message = '2WEEKS'
    if alert_message in request.vars.Body:
        alert_to = alert_to_2_week_email
        alert_subject = "PLUS Alert - 2 Week Alert"
        #alert_body = "%s sent the following alert: %s, their 4 week point level is: %s, message ID: %s, click here to send points: http://plus.laundrylux.com/plusportal2/plusc/emailtest" % (location_name, request.vars.Body, location_four_week_point_level, sms_message_id)
        send_email(alert_to, alert_subject, alert_body)
        
    alert_message = 'POINTS BELOW LOW LEVEL'
    if alert_message in request.vars.Body:
        alert_to = alert_to_1_week_email
        alert_subject = "PLUS Alert - 1 Week Alert"
        alert_body = "%s sent the following alert: %s, their 4 week point level is: %s, message ID: %s" % (location_name, request.vars.Body, location_four_week_point_level, sms_message_id)
        send_email(alert_to, alert_subject, alert_body)
    
    resp = twiml.Response()
    # resp.sms("hello")
    
    return str(resp) # dict()
    
@auth.requires_login()
def add_location():
    form=SQLFORM(db.t_plus_location)
    if form.process().accepted:
        session.flash = 'form accepted'
        #redirect(URL('viewlocations'))
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def manage_table():
    grid=SQLFORM.smartgrid(db.t_plus_location,
        onupdate=auth.archive)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)
        
@auth.requires_login()
def manage_distributors():
    grid=SQLFORM.smartgrid(db.t_plus_distributor,
        onupdate=auth.archive)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()
def manage_locations():
    fields = (db.t_plus_location.f_name, db.t_plus_location.f_location_id, db.t_plus_location.f_city, db.t_plus_location.f_contact_name, db.t_plus_sms_message.id) #, db.t_plus_location_contact.f_contact, db.t_plus_machine.f_name, db.t_plus_contact.f_name, db.t_plus_distributor.f_name)
    
    if 'view' not in request.args:
        #db.t_plus_location.f_name.readable = False
        #db.t_plus_location.f_location_id.readable = False
        db.t_plus_location.f_street.readable = False
        db.t_plus_location.f_street2.readable = False
        #db.t_plus_location.f_city.readable = False
        db.t_plus_location.f_status.readable = False
        db.t_plus_location.f_zip.readable = False
        db.t_plus_location.f_sms_phone_number.readable = False
        db.t_plus_location.f_sms_provider.readable = False
        #db.t_plus_location.f_contact_name.readable = False
        db.t_plus_location.f_contact_phone.readable = False
        db.t_plus_location.f_four_week_point_level.readable = False
        db.t_plus_location.f_distributor.readable = False
    
    grid=SQLFORM.smartgrid(db.t_plus_location, 
        #fields=fields,
        maxtextlength=70, 
        exportclasses=defExportClasses, showbuttontext=defShowbuttontext,
        #create=False,editable=False,
        #links = [lambda row: A('+',callback=URL('cart_callback',vars=dict(id=row.id,action='add')))]
    )
        #linked_tables=['t_plus_machine', 't_plus_sms_message'])
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()
def manage_contacts():
    grid=SQLFORM.smartgrid(db.t_plus_contact)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()
def manage_location_contacts():
    grid=SQLFORM.smartgrid(db.t_plus_location_contact)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)
               
@auth.requires_login()
def manage_machines():
    grid=SQLFORM.smartgrid(db.t_plus_machine)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()           
def manage_messages2():
    # this is old action - tbd
    
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        linked_tables=['t_plus_location'],
        orderby=~db.t_plus_sms_message.created_on)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()           
def manage_messages():
    
    fields = (db.t_plus_sms_message.f_body, db.t_plus_sms_message.f_location, db.t_plus_sms_message.f_status,
        db.t_plus_sms_message.f_direction, db.t_plus_sms_message.created_on, db.t_plus_sms_message.f_points)
    
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        fields=fields,
        linked_tables=['t_plus_location'],
        maxtextlength=70, 
        orderby=~db.t_plus_sms_message.created_on)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)
                        
@auth.requires_login()           
def manage_new_msgs():  
    query = db.t_plus_sms_message.f_status == 'New'
    constraints = {'t_plus_sms_message':query}
    
    fields = (db.t_plus_sms_message.f_body, db.t_plus_sms_message.f_location, db.t_plus_sms_message.f_status,
        db.t_plus_sms_message.f_direction, db.t_plus_sms_message.created_on, db.t_plus_sms_message.f_points)
    
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        constraints=constraints,
        fields=fields,
        linked_tables=['t_plus_location'],
        maxtextlength=70, 
        orderby=~db.t_plus_sms_message.created_on)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)
        
@auth.requires_login()           
def manage_alert_msgs():  
    query = db.t_plus_sms_message.f_body.contains(['2WEEKS','POINTS BELOW LOW LEVEL','0 32'], all=False)
    constraints = {'t_plus_sms_message':query}
    
    fields = (db.t_plus_sms_message.id, db.t_plus_sms_message.f_body, db.t_plus_sms_message.f_location, db.t_plus_sms_message.f_status,
        db.t_plus_sms_message.f_direction, db.t_plus_sms_message.created_on, db.t_plus_sms_message.f_points)
    
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        constraints=constraints,
        fields=fields,
        linked_tables=['t_plus_sms_message'],
        maxtextlength=70, 
        orderby=~db.t_plus_sms_message.created_on)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()           
def manage_error_msgs():  
    query = db.t_plus_sms_message.f_body.contains(['error'], all=False)
    constraints = {'t_plus_sms_message':query}
    
    fields = (db.t_plus_sms_message.f_body, db.t_plus_sms_message.f_location, db.t_plus_sms_message.f_status,
        db.t_plus_sms_message.f_direction, db.t_plus_sms_message.created_on, db.t_plus_sms_message.f_points)
    
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        constraints=constraints,
        fields=fields,
        linked_tables=['t_plus_location'],
        maxtextlength=70, 
        orderby=~db.t_plus_sms_message.created_on)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)

@auth.requires_login()           
def manage_sent_msgs():  
    query = db.t_plus_sms_message.f_direction == 'Sent'
    constraints = {'t_plus_sms_message':query}
    
    fields = (db.t_plus_sms_message.f_body, db.t_plus_sms_message.f_location, db.t_plus_sms_message.f_status,
        db.t_plus_sms_message.f_direction, db.t_plus_sms_message.created_on, db.t_plus_sms_message.f_points)
    
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        constraints=constraints,
        fields=fields,
        linked_tables=['t_plus_location'],
        maxtextlength=70, 
        orderby=~db.t_plus_sms_message.created_on)
    func = request.function
    if (func == 'wiki'):
        return grid
    else:
        return dict(form=grid)
        
def chart():
    chartdata = (['Loc A', 3],
          ['Loc B', 1],
          ['Loc C', 4],
          ['Loc D', 1],
          ['Loc E', 2])
    #chartdata=chartdata, charttitle='Messages by Loc'
    return dict(charttitle='Messages by Loc')
