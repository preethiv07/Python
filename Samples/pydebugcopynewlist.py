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
    fh.close()    #donot use in finally clause as if a file name that doesnt exist is entered in input, it cannot close it.
#finally:    
gradesdata=[]
if data: # as long there is data in the list "data"
    for student in data:
        try:
            #print (student[0:2])
            #print (student[2])
            #gradesdata.append([student[0:2],student[2]]) # this fails is student doesnt have two names
            name=student[0:-1]
            grades=int(student[-1])
            gradesdata.append([name,[grades]]) # captures name in case of no last name and has grades
      #  except IndexError:
       #     gradesdata.append([student[0:2],[]])  # in case no grades to the students, get empty list &add to student
        except ValueError:
            gradesdata.append([student[:],[]])  # in case no grades for student

print("data: " ,data)
print("gradesdata" ,gradesdata)

#value error - type conversion
#name error = variable used before defining
#attribute error = with class
#type error = objects of type int cannot be used for len,passing a objects to a function that except other data type
# say, passing int([l1,l2]) - passing list to int where string is expected


#why should fh.close() should be in else clause and not fianlly
#if in fianlly will cause name error