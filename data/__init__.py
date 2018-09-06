import os
import json


def logerr(info):
    print(info)
    exit(1)

class dataObj():
    def __init__(self):
        self.path = []
        self.size = 0

    def checkAttr(self):
        if hasattr(self, 'path'):
            for i in self.path:
                if not os.path.exists(i):
                    logerr('path is not exist: %s' % i)
                else:
                    DirSize = self.statDir(i)
                    if hasattr(self, 'size') and self.size != 0:
                        if self.size != DirSize:
                            logerr('%s size not equal %s' % (i, self.size))
                    else:
                        self.size = DirSize

    def archive(self):
        tmpdata = {}
        for i in ['path', 'size', 'pid']:
            if hasattr(self,i) :
                tmpdata[i] = getattr(self, i)
        print(json.dumps(tmpdata, sort_keys=True, indent=4, separators=(',', ': ')))

    def addPath(self, path):
        if path in self.path:
            logerr('Err: exist path: %s' % path)
        else:
            if os.path.exists(path):
                self.path.append(path)
            else:
                logerr('path not exist, need cp')

    def statDir(self, path):
        sum = 0
        if os.path.isdir(path):
            files = []
            for i in self.getAllFile(path,files):
                sum += os.stat(i).st_size
        else:
            logerr('path is not direct')
        return sum

    def getAllFile(self,path,files):
        if os.path.isdir(path):
            for i in os.listdir(path):
                i = os.path.join(path, i)
                if os.path.isfile(i):
                    files.append(i)
                elif os.path.isdir(i):
                    self.getAllFile(i,files)
        return files

    def cpFile(self):
        os.system("cp -r %s %s",)
