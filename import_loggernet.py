#!/usr/bin/python26

__author__ = 'ktarbet'

import glob
import sys
import loggernet
import agrimet
import hydromet as hydromet
import os

def main():

    path = '/var/opt/CampbellSci/LoggerNet'

    if not os.path.exists(path+"/attic"):
        os.mkdir(path+"/attic")

    hydromet_data = []
    for site in agrimet.sites:
        for fn in glob.glob1(path,site+"_*.dat"):
            print "reading "+fn
            lnf = loggernet.LoggerNetFile(path+"/"+fn)
            if not lnf.valid:
                continue
            hydromet_data.extend(lnf.create_hydromet_file())
            # move file to attic
            os.rename(path+"/"+fn,path+"/attic/"+fn)


    if len(hydromet_data) >0:            
        hydromet.import_instant_data(hydromet_data)

if __name__ == '__main__':
    main()
