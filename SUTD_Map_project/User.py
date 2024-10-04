selection_yes=['1','y','Y','Yes','yes']
selection_no=['0','n','N','No','no']

class User():
    def __init__(self):
        self.clearance_card={"Basic"}
        self.clearance_list=["Fablab_basic","Fablab_Woodwork","Fablab_Metalwork","Hostel_55","Hostel_57","Hostel_59","Freshmore_Cohortclass", "42SG_Access",\
                             "DAI_Studio", "Auditorioum_Backstage_Alley", "Hobby_Shop"]
        self.freshmore_preset_list=["Fablab_basic","Freshmore_Cohortclass"]

    def display_clearances(self):
        print(self.clearance_card)

    def add_clearance(self):
        for i, clearance in enumerate(self.clearance_list):
            print("{:02d}\t{}".format(i, clearance))
        while True:
            try:
                selection = int(input("\nPick a Clearance: "))
                if 0 <= selection < len(self.clearance_list):
                    self.clearance_card.add(self.clearance_list[selection])
                    break
                else:
                    print("Out of index")
            except ValueError:
                print("Not a valid input")

        print("\nConfirm selection \n{:02d}\t{}?\n".format(selection, self.clearance_list[selection]))
        sel = input("y/n: ")
        if sel in selection_yes:
            print("Selected {}\n".format(self.clearance_list[selection]))
            return self.clearance_list[selection]
        elif sel in selection_no:
            return self.add_clearance()
        else:
            print("Not a valid input \nExiting add_clearance tool\n")

    def remove_clearance(self):
        cc_list = list(self.clearance_card)
        to_remove=""
        for i in range(len(cc_list)):
            print("{:02d}\t{}".format(i, cc_list[i]))

        while True:
            try:
                selection=int(input("\nSelect clearance to remove: "))
                if selection>-1 and selection<len(cc_list):
                    to_remove=cc_list[selection]
                    break
                else:
                    print("out of index")
            except ValueError:
                print("Not a valid input")

        print("\nConfirm selection {}?\n".format(to_remove))
        sel=input("y/n: ")
        if sel in selection_yes:
            print("Removing {} from clearance\n".format(to_remove))
            self.clearance_card.remove(to_remove)
        elif sel in selection_no:
            return self.query_vertex_Prefix()
        else:
            print("Not a valid input \nExiting remove_clearance tool\n")
