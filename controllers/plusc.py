from twilio import twiml
from twilio.rest import TwilioRestClient

# coding: utf8
# try something like

def addlocation():
    form=SQLFORM(db.t_plus_location)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('viewlocations'))
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill the form'
    return dict(form=form)
    
def manage_locations():
    grid=SQLFORM.smartgrid(db.t_plus_location,
        linked_tables=['t_plus_machine'])
    return grid
    
def manage_messages():
    grid=SQLFORM.smartgrid(db.t_plus_sms_message,
        linked_tables=['t_plus_location'])
    return grid
    
def receivesms():
    ''' receive sms message, insert into db, reply for confirmation '''
    # test with plusportal2/plusc/receivesms?From=15167217331&To=15161231234&Body=Hello
    
    db.t_plus_sms_message.insert(
        f_from = request.vars['From'],
        f_to = request.vars.To,
        f_body = request.vars.Body)
        
    #sender = request.vars['From'][-10:]+'@vtext.com'
    #mail.send([sender],'hello',request.vars.Body)
    
    resp = twiml.Response()
    # resp.sms("hello")
    
    return str(resp) # dict()
