import os
import json


def logerr(info):
    print(info)
    exit(1)


def logout(info):
    print(info)


class dataObj():
    def __init__(self,id='temp.txt'):
        self.path = []
        self.size = 0
        self.dataSource = '.'
        self.id = id

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

    # save dataobj
    def archive(self):
        tmpdata = {}
        for i in ['path', 'size', 'pid']:
            if hasattr(self,i) :
                tmpdata[i] = getattr(self, i)

        with open(os.path.join(self.dataSource, self.id + ".json"), 'w') as f:
            f.write(json.dumps(tmpdata, sort_keys=True, indent=4, separators=(',', ': ')))

    # clone path
    def addPath(self, path):
        if path in self.path:
            logerr('Err: exist path: %s' % path)
        else:
            if os.path.exists(path):
                self.path.append(path)
            else:
                self.cloneFile(path)
                self.path.append(path)

    # stat dir size
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

    def cloneFile(self, newpath):
        oldpath = self.findoldpath()
        os.system("cp -r %s %s" % (oldpath, newpath))
        logout("CMD: cp -r %s %s" % (oldpath, newpath))

    def findoldpath(self):
        for i in self.path:
            if os.path.isdir(i):
                return i
