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

@auth.requires_login()
def send_message():
    db.t_plus_sms_message.f_from.writable = False
    db.t_plus_sms_message.f_location.default = 1
    db.t_plus_sms_message.f_status.default = 'Processed'
    db.t_plus_sms_message.f_direction.default = 'Sent'
    form=SQLFORM(db.t_plus_sms_message, fields=['f_location', 'f_body'])
    if form.process().accepted:
        session.flash = 'form accepted'
        
        locNumber = db(db.t_plus_location.id==form.vars.f_location).select()
        # test credentials
        # account = "ACc3bf197710521ed42649640d90bc5b82"
        # token = "c621b2222995adfca2a466fe389f26f6"
        # live credentials
        account = "AC57a31d8a4c47e868f90f8bae98dd09d6"
        token = "a2bc850976c783b714a99c749ca01d62"
        client = TwilioRestClient(account, token)
        message = client.sms.messages.create(to=locNumber[0].f_sms_phone_number, from_="+15162047575",
                                     body=form.vars.f_body)
                                     
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill the form'
    return dict(form=form)

def receivesms():
    ''' receive sms message, insert into db, reply for confirmation '''
    # test with plusportal2/plusc/receivesms?From=15167217331&To=15162047575&Body=Hello
    
    db.t_plus_sms_message.insert(
        f_from = request.vars['From'],
        f_to = request.vars.To,
        f_body = request.vars.Body)
        
    #sender = request.vars['From'][-10:]+'@vtext.com'
    #mail.send([sender],'hello',request.vars.Body)
    
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
    grid=SQLFORM.smartgrid(db.t_plus_location, 
        exportclasses=defExportClasses, showbuttontext=defShowbuttontext,
        #create=False,editable=False,
        links = [lambda row: A('+',callback=URL('cart_callback',vars=dict(id=row.id,action='add')))]
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
def manage_messages():
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        linked_tables=['t_plus_location'])
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
