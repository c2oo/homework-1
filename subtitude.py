#!/usr/bin/env python
#-*-coding:utf8-*-

""" 2015-04-16 anning """


def PackageManage(package,handle):
    pack = getattr(__import__('lib.' + package),package)
    return getattr(pack,handle)

class InsertHandle(object):

    """  Data iteration for insert """

    def __init__(self,files,flag,after):
        self.files = files
        self.flag = int(flag)
        self.after = after
        self.offset = 10
        self.intermediate = after

    def __iter__(self):
        return self

    def next(self):
        with file(self.files,'r+') as f:
            if self.offset > self.flag:
                f.seek(self.flag)
                data = f.read(self.offset-len(self.after))
                NewData = self.intermediate + data
                self.intermediate = f.read(len(self.after))
                f.seek(self.flag)
                f.write(NewData)
                if not self.intermediate:
                    raise StopIteration();
                self.flag = f.tell()

            else:
                self.offset += 10

class ReplaceHandle(object):

    """  Data iteration for replace """

    def __init__(self,files,before,afer):
        self.files = files
        self.before = before
        self.afer = afer
        self.sk = 0
        self.LastFile = ''

    def __iter__(self):
        return self

    def next(self):
        offset = 5
        with file(self.files,'r+') as f:
            f.seek(self.sk)
            data = f.read(offset)

            if data:
                if self.before in data:
                    NewData = data.replace(self.before,self.afer)
                else:
                    NewData = data

                TotalData = self.LastFile + NewData
                self.LastFile = NewData

                if self.before in TotalData:
                    NewTotalData = TotalData.replace(self.before,self.afer)
                    f.seek(self.sk - offset)
                    f.write(NewTotalData)
                else:
                    f.seek(self.sk)
                    f.write(NewData)

                self.sk = f.tell()

            else:
                raise StopIteration();

CallbackBase = PackageManage('callback','CallbackBase')

class MainHandle(CallbackBase):

    """ handle entrance """

    Replace = 'replace'
    Insert = 'insert'

    @CallbackBase.callback(Replace)
    def handler1(self, am1 = None, am2 = None, am3 = None):
        Runner = ReplaceHandle(am1,am2,am3)
        for i in Runner:
            pass
        return None

    @CallbackBase.callback(Insert)
    def handler2(self, am1 = None, am2 = None, am3 = None):
        Runner = InsertHandle(am1,am2,am3)
        for i in Runner:
            pass
        return None

    def run(self, event, am1 = None, am2 = None, am3 = None):
        self.dispatch(event)(am1,am2,am3)

if __name__ == "__main__":
    a = MainHandle()
    import sys

    if MainHandle.Replace == sys.argv[1]:
        a.run(MainHandle.Replace, sys.argv[2], sys.argv[3], sys.argv[4])

    elif MainHandle.Insert == sys.argv[1]:
        a.run(MainHandle.Insert, sys.argv[2], sys.argv[3], sys.argv[4])

