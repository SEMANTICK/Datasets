#Note you have to save this py file on the desktop
#G005 is removed due to some issues
#see that the files are stored in the following fashion  Data(Folder)>A001.txt,A002.txt....

import pandas as pd;
L=["A001","A002","A003","A004","A005","G001","G002","G003","G004","G006","G007","H001","H002","H003","H004","H005"] #replace the values in the list with the names of your txt files
# readinag given csv file 
# and creating dataframe
print("****************\n")
for i in L:
    url="../Desktop/Data/"+i+"/"+i+".txt"
    dataframe1 = pd.read_csv(url) 
      # storing this dataframe in a csv file 
    dataframe1.to_csv(i+".csv",index = None)
    print("*", end='')

print("completed")
