import os, sys

sys.path.append('/4gtss/mount/site')
sys.path.append('/4gtss/mount/site/npg')
os.environ['DJANGO_SETTINGS_MODULE'] = 'npg.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import npg.monitor
npg.monitor.start(interval=1.0)


#The below line has been added by bahaa
#sys.stdout = sys.stderr
