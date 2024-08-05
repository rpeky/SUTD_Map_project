class Query():
    def __init__(self, idlkup):
        self.dd_locationid = idlkup
        print('test query class')
        print(self.dd_locationid)

    def __del__(self):
        print('test del query class')
