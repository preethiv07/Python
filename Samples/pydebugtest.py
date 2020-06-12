data =[]
file_name =input("enter file name :")
try:
    fh=open(file_name,'r')
except IOError:
    print("IO Error",file_name)
else:
    print("can open",file_name)
    for new in fh:
        if new !="\n":
            add = new[:-1].split(',' ) #remove training \n
            data. append(add)#add to a new list
finally:
    fh.close()    