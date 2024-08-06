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
        print("Welcome to Query page\n")

    def display_options_initial(self):
        dd_zones={
        "LEVEL_1":['1'],
        'Building_1':['2','3','4','5','6','7'],
        'Building_2':['2','3','4','5','6','7'],
        'Building_3':['2','3','4','5','6','7'],
        'Building_5':['2','3','4','5','6'],
        'Block_51':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_53':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_55':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_57':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_59':['2','3','4','5','6','7','8','9','10','11','12'],
        'Sports_and_Recreation_Centre':['2','3']
        }
        print("test\n")

    def tempwaitinput(self):
        temp = input("Enter any key to continue:")
