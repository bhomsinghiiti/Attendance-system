from flask import Flask, render_template,redirect,url_for,request,send_file
app=Flask(__name__)
import csv
import os
path="C:\\Users\\Addict\\Desktop\\fhaltukaam\\Attendance-system\\"  # plese enter your own path in place of this
def file_ex(a,b):
    if a.split(".")[1]=="txt" and b.split(".")[1]=="csv":
        return True
    else:
        return False

def get_key(my_dict,val):
    for i in my_dict.keys():
        if my_dict[i]==val:
            return i


def sender(a):
    if a[-9:]>"07:00 AM" and  a[-9:]<"11:59 PM":
        return True
    else:
        return False

def attendence():
    # first open csv file and store the all student roll no in a list 
    f2=open("refrence.csv","r")
    f2=csv.reader(f2)
    next(f2)
    SList=[]
    for i in f2:
        SList.append(i[1])    
    # open attendence.txt file and store all the roll no's of the present student in the another list
    f=open("attendence.txt","r")
    s=" "
    ps_dict={}
    while s:
        s=f.readline()
        if sender(s):
            name=s[0:-9]
            s=f.readline()
            ls=s.split()
            for i in ls:
                if i in SList:
                    # some roll no is written by two different students
                    #     break
                    if name in ps_dict.values():
                        j=get_key(ps_dict,name)
                        if j!=i:
                            ps_dict[j]="proxy "+name+","+i+","+j
                            if i not in ps_dict.keys():
                                 ps_dict[i]="proxy "+name+","+i+","+j
                            break
                    else:
                        ps_dict[i]=name

    # create or open updated.csv file and store ....
    f3=open("updated.csv","w",newline="")
    f3=csv.writer(f3)

    # again open refrence.csv file and 
    f4=open("refrence.csv","r")
    f4=csv.reader(f4)


    # for printing the header looping only on line 
    for i in f4:
        f3.writerow(i)
        break

    #for print rest of the data in  the file 
    for i in f4:
        if i[1] in ps_dict.keys():
            if ps_dict[i[1]][0:5]=="proxy":
              i[-1]=ps_dict[i[1]]
            else:
                i[-1]="1"
        else:
            i[-1]="0"
        f3.writerow(i)

@app.route('/',methods=["GET","POST"])
def hello():
    if request.method=="POST":
        file1=request.files["textfile"]
        file2=request.files["csvfile"]
        if file_ex(file1.filename,file2.filename):
            file1.save(os.path.join(path,"attendence.txt"))
            file2.save(os.path.join(path,"refrence.csv"))
            attendence()
            return render_template("download.html")
        else:
            ms="please enter valid file extention "
            return render_template('home.html',ms=ms)
    return render_template('home.html')
@app.route('/getfile')
def home():
    return render_template('download.html')

@app.route('/download')
def download_file():
    return send_file("updated.csv",as_attachment=True)


if __name__=='__main__':
    app.run(debug=True)
