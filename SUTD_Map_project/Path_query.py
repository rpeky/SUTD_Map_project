class Query():
    def __init__(self, idlkup):
        self.dd_locationid = idlkup
        print('test query class')
        print(self.dd_locationid)
        self.welcome_message()
        self.tempwaitinput()

    def __del__(self):
        print('test del query class')

    def welcome_message(self):
        print("placeholder message hello owo\n")

    def tempwaitinput(self):
        temp = input("Enter any key to continue:")
