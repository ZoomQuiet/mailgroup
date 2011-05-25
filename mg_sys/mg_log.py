import logging
import sys
import os
import os.path

path = os.path.normpath(os.path.join(os.getcwd(), __file__))
path = os.path.split(path)[0]

fmt = '%(asctime)s %(name)s %(levelname)s:%(message)s'
datefmt = '%H:%M:%S %y/%m/%d'

mailFormatter = logging.Formatter(fmt, datefmt)
mailHandler = logging.FileHandler(path + '/mail.log',mode='a',encoding='utf8')
mailHandler.setLevel(logging.INFO)
mailHandler.setFormatter(mailFormatter)

sysFormatter = logging.Formatter(fmt, datefmt)
sysHandler = logging.FileHandler(path + '/mg_sys.log',mode='a',encoding='utf8')
sysHandler.setLevel(logging.INFO)
sysHandler.setFormatter(sysFormatter)

shellFormatter = logging.Formatter(fmt, datefmt)
shellHandler = logging.StreamHandler(sys.stdout,)
shellHandler.setLevel(logging.INFO)
shellHandler.setFormatter(shellFormatter)

def sendLogger():
    sendLogger = logging.getLogger('send')
    sendLogger.setLevel(logging.INFO)
    sendLogger.addHandler(mailHandler)
    sendLogger.addHandler(shellHandler)
    return sendLogger

def receiveLogger():
    receiveLogger = logging.getLogger('receive')
    receiveLogger.setLevel(logging.INFO)
    receiveLogger.addHandler(mailHandler)
    receiveLogger.addHandler(shellHandler)
    return receiveLogger

def sysLogger():
    sysLogger = logging.getLogger('sysLogger')
    sysLogger.setLevel(logging.INFO)
    sysLogger.addHandler(sysHandler)
    sysLogger.addHandler(shellHandler)
    return sysLogger

