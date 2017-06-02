__author__ = 'ktarbet'

import loggernet

lnf = loggernet.LoggerNetFile("c:/temp/file1.txt")

x = lnf.create_hydromet_file()

for a in x:
    print a