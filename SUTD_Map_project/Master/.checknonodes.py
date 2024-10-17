import os
import json

checkpath = os.path.join(os.getcwd(), "Building_2_Level_4.json")
f = open(checkpath)
checking = json.load(f)

print(len(checking))
