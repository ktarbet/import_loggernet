__author__ = 'ktarbet'

import tempfile
import os
import datetime
import sys
def import_instant_data(data):

    temp = tempfile.NamedTemporaryFile()
    temp.file.write("yyyyMMMdd hhmm cbtt     PC        NewValue   OldValue   Flag User: loggernet\n")
    for line in data:
        temp.file.write(line+'\n')
    temp.file.close()

    remote_fn = "/huser1/incoming/instant_"+\
                datetime.datetime.now().strftime("%b%d%Y%H%M%S").lower()+".txt"

    cmd = "/usr/bin/scp -q "+ temp.name  +" agrimet@pnhyd0.pn.usbr.gov:"+remote_fn
    print cmd
    rval = os.system(cmd)
    print 'scp returned '+str(rval)
    
