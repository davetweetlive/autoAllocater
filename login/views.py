from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.template import loader

from .forms import LoginForm

###################################################################################
#                               State and configuration variables
###################################################################################

# Current status of the page.
PAGE_OK = 0
LAST_PAGE_STATUS = PAGE_OK

# Status codes for verification of credentials.
LOGIN_OK = 1
USER_NOEXIST = -1
INVALID_PWD = -2

TEMPLATES_DIR = 'login/templates/www_dave/'

###################################################################################
#                               Utility functions
###################################################################################

# Verify username and password from the text file operators.txt
def verifyCredentials(uname, pwd):
    ret = {}
    print('---------------'+uname+','+pwd)
    global LAST_PAGE_STATUS, PAGE_OK, LOGIN_OK, USER_NOEXIST, INVALID_PWD
    
    with open((TEMPLATES_DIR + 'operators.txt'), 'r') as db_file:
        while True:
            # This list holds the user data for each user at each iteration.
            section = {}
            l = db_file.readline()
            
            # EOF
            if l is '':
                break
            
            # Get the current user's detail from a'{' to '}' line.
            if l.strip() == '{':
                while True:
                    line = db_file.readline().strip()
                    #print('line:' + line)
                    if line and (line is not '}'):
                        section[line.split(':')[0]] = line.split(':')[1]
                    if line is '}':
                        break
            
            # Now compare the uname and pwd.
            if (section['uname'] == uname) and (section['pwd'] == pwd):
                ret = section
                LAST_PAGE_STATUS = LOGIN_OK
                print('LOGIN_OK')
                break
            elif section['uname'] != uname:
                LAST_PAGE_STATUS = USER_NOEXIST
                #print('USER_NOEXIST')
            elif section['pwd'] != pwd:
                LAST_PAGE_STATUS = INVALID_PWD
                #print('INVALID_PWD')
    
    return ret

def getIncompleteTicket():
    print('In getIncompleteTicket():')
    tktId = ''
    with open(TEMPLATES_DIR + 'tasks.txt', 'r') as tktFile:
        while True:
            # This list holds the user data for each user at each iteration.
            section = {}
            l = tktFile.readline()
            
            # EOF
            if l is '':
                break
            
            # Get the current user's detail from a'{' to '}' line.
            if l.strip() == '{':
                while True:
                    line = tktFile.readline().strip()
                    #print('line:' + line)
                    if line and (line is not '}'):
                        section[line.split(':')[0]] = line.split(':')[1]
                    if line is '}':
                        break
            print(section)
            print(section['Status'].upper())
            # Check if ticket is INCOMPLETE
            if section['Status'].upper() == 'INCOMPLETE':
                tktId = section['ID']
                print('tktId:' + tktId)
                break
        
    return tktId

def setTicketComplete(tktId=b''):
    pass
    
###################################################################################
# ------------------------- Views definitions -------------------------
###################################################################################

def index(request):
    # If already logged in...
    
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('YES POST!')
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            formData = form.cleaned_data
            #print(formData)
            
            # Verify username and password from the text file operators.txt
            userInfo = verifyCredentials(formData['uname'], formData['pwd'])
            print('userInfo:' + str(userInfo))
            print('LAST_PAGE_STATUS:' + str(LAST_PAGE_STATUS))
            if LAST_PAGE_STATUS == LOGIN_OK:
                #return render(request, 'www_dave/home.html', userInfo)
                template = loader.get_template('www_dave/home.html')
                return HttpResponse(template.render(userInfo, request))
            elif LAST_PAGE_STATUS == USER_NOEXIST:
                return render(request, 'www_dave/index.html', {'form': form, 'status':USER_NOEXIST})
            elif LAST_PAGE_STATUS == INVALID_PWD:
                return render(request, 'www_dave/index.html', {'form': form, 'status':INVALID_PWD})
    
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'www_dave/index.html', {'form': form})

def home(request):
    print('In home(request)')
    if len(request.POST) is 0:
        print('Uuum!')
        raise PermissionDenied
    print('OK!')
    tktId = getIncompleteTicket()
    print('tktId: ' + str(tktId))
    return render(request, 'www_dave/home.html', {'TicketID':tktId})