
import agrimet

__author__ = 'ktarbet'

import os
import datetime
import time

def read_variable_names(line):
    _v = line.rstrip('\r\n')
    _v = _v.split(',')
    for i in range(len(_v)):
        #print "|" + _v[i] + "|"
        _v[i] = _v[i].strip('"')
        #print "|" + _v[i] + "|"
    return _v



def valid_pcode(pcode):
    return pcode in agrimet.pcodes

def valid_site(cbtt):
    return cbtt in agrimet.sites


#def get_flag(pcode, value):
#    flag = '-01'
#    with open('quality_limits.csv', 'r') as file:
#        for line in file:
#            _pcode, _hval, _lval = line.rstrip('\r\n').split(',')
#            if pcode == _pcode:
#                if float(value) > float(_hval):
#                    flag = '-22'
#                elif float(value) < float(_lval):
#                    flag = '-20'
#    return flag


class LoggerNetFile:
    """
    manages a loggernet file
    "TOACI1","Agtest","Min15"
    "TMSTAMP","RECNBR","Batt_volt","OB_Avg","OBX_Max","OBN_Min","TU_Avg","TUX_Max","TUN_Min","EA","TP_Avg","WindSp_WVT","WD","WG_Max","WS_Avg","PC","SQ","UI","SI","ETo","SQco","ETr","SQcr"
    "2012-10-25 14:00:00",2124,13.44427,60.02,60.40305,59.67196,34.85878,35.64064,34.42216,0.6231159,32.20473,0.8211018,0,1.5344,0.8211015,9.403034,5535.25,386.3387,40.66694,6.50607,1.462601,6.944839,1.462601
    """

    quality_limits = {}

    def __init__(self, filename):
        _file = open(filename,'r')
        self.lines = _file.readlines()
        _file.close()
        if len(self.lines) < 3:
            print "error: not enough data"
            raise StandardError()

        self.header = self.lines[0].replace('"','').split(',')
        self.file_format = self.header[0]
        self.cbtt = self.header[1]
        self.variable_names = read_variable_names(self.lines[1])
        self.valid = True
        if self.file_format != "TOACI1" :
            self.valid = False
            print "skipping invalid file: "+filename
            #print filename

        if len(LoggerNetFile.quality_limits) == 0 :
            with open('/home/agrimet/bin/quality_limits.csv', 'r') as f:
                next(f)
                for line in f:
                    _pcode, _hval, _lval = line.rstrip('\r\n').split(',')
                    LoggerNetFile.quality_limits[_pcode] = [float(_hval), float(_lval)]
            print "read "+str(len(LoggerNetFile.quality_limits)) +" entries in quality_limits.csv"



    def get_flag(self, pcode, value):
        flag = '-01'
        if pcode in LoggerNetFile.quality_limits:
            if float(value) > LoggerNetFile.quality_limits[pcode][0]:
                print pcode+" "+value + " +"
                flag = '-22'
            elif float(value) < LoggerNetFile.quality_limits[pcode][1]:
                print pcode+" "+value + " -"
                flag = '-20'
        return flag

    def create_hydromet_file(self):
        """
        $ ty INSTANT_KTARBETSEP242012075440.TXT;
        yyyyMMMdd hhmm cbtt     PC        NewValue   OldValue   Flag user:ktarbet
        2012SEP17 1830 UNY      FB        3785.05    3785.07    -03
        2012SEP17 1845 UNY      FB        3785.04    3785.07    -03
        2012SEP17 1900 UNY      FB        3785.04    3785.07    -03
        2012OCT25 1245 AGTEST   OB        62.26      998877.00  -01
        2012OCT25 1245 AGTEST   ETR       1190.89    998877.00  -01
        """

        rval=[]
        for line in self.lines[2:]:
            vals = line.replace('"','').rstrip('\r\n').split(',')
            t = datetime.datetime.strptime(vals[0],"%Y-%m-%d %H:%M:%S")
            for pcode, num in zip( self.variable_names,vals):
                if valid_pcode(pcode)  and valid_site(self.cbtt):
                    flag = self.get_flag(pcode.upper(), num)
#		    print ':'+num+':'
                    if num == 'NAN':
                        num = 998877
                    str = t.strftime("%Y%b%d %H%M").upper() +\
                          ' '+self.cbtt.upper().ljust(8)+\
                          ' '+ pcode.upper().ljust(9)+\
                          ' '+("%.2f" % float(num)).ljust(10) +\
                          ' '+("%.2f" % 998877).ljust(10) +\
                          ' '+flag
                    rval.append(str)

        return rval










