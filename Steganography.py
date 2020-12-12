import PIL.Image 
from tkinter import *
from tkinter import filedialog

def fun(n):
    n="0"*(8-len(str(n)))+str(n)
    t1=(int(n[0]),int(n[1]),int(n[2]),int(n[3]))
    t2=(int(n[4]),int(n[5]),int(n[6]),int(n[7]))
    return t1,t2

def bun(t1,t2):
    n = int((str(t1[0])+str(t1[1])+str(t1[2])+str(t1[3])+str(t2[0])+str(t2[1])+str(t2[2])+str(t2[3])).lstrip('0'))
    return n


def bin_8(n):
    b = '{0:b}'.format(n)
    return '0'*(8 - len(b)) + b 

def Encrypt(name, ext, text):
    img = PIL.Image.open(name + ext)
    img.convert("RGBA").save(name+"_png"+".png")
    img = PIL.Image.open(name +"_png"+ ".png")
    pixels = img.load()
    width, height = img.size
    # print(width, height
    l = len(text)
    t1, t2 = fun(l)
    ascii_vals = [ord(i) for i in text]
    # print(ascii_vals)
    pixels[width - 1, height - 1] = t2
    pixels[width - 2, height - 2] = t1
    x, y = 0, 0
    #print(img.getpixel((width - 1, height - 1)))
    for i in ascii_vals:
        tup = img.getpixel((x, y))
        bn = bin_8(i)
        tup2 = (bin_8(tup[0]), bin_8(tup[1]), bin_8(tup[2]), bin_8(tup[3]))
        tup3 = (tup2[0][:6]+bn[:2],tup2[1][:6]+bn[2:4],tup2[2][:6]+bn[4:6],tup2[3][:6]+bn[6:])
        tup4 = (int(tup3[0],2),int(tup3[1],2),int(tup3[2],2),int(tup3[3],2))
        pixels[x, y] = tup4
        #print(img.getpixel((x, y)),x,y)
        if x == width - 1:
            y += 1
            x = 0
        else:
            x += 1
    img.save(name+"_e"+".png")


def Decrypt(name,ext):
    img = PIL.Image.open(name + ext)
    width, height = img.size
    text = ""
    t2 = img.getpixel((width - 1, height - 1))
    t1= img.getpixel((width - 2, height - 2))
    l = bun(t1,t2)
    x, y = 0, 0
    for i in range(l):
        tup = img.getpixel((x, y))
        tup1 = (bin_8(tup[0]),bin_8(tup[1]),bin_8(tup[2]),bin_8(tup[3]))
        c = tup1[0][6:]+tup1[1][6:]+tup1[2][6:]+tup1[3][6:]
        # print(tup)
        text += chr(int(c,2))
        if x == width - 1:
            y += 1
            x = 0
        else:
            x += 1
    return text

def fildia():
    f_name =  filedialog.askopenfilename(initialdir =  "/", title = "Select an Image File", filetype =(("png files","*.png"),("jpeg files","*.jpg")) )
    sv.set(f_name)
    
def en():
    text = e1.get("1.0",END)
    e1.delete('1.0',END)
    f = sv.get()
    name = f.split('.')[0]
    ext = '.'+f.split('.')[1]
    try: 
        Encrypt(name,ext,text)
        l1.config(text="Sucess")
    except:
        l1.config(text="Failed")
    

def de():
    e1.delete('1.0',END)
    f = sv.get()
    name = f.split('.')[0]
    ext = '.'+f.split('.')[1]
    try:
        text = Decrypt(name,ext)
        e1.insert('1.0',text)
        l1.config(text="Sucess")
    except:
        l1.config(text="Failed")

root = Tk()
root.title("Steganography")
l = Label(root,text="Steganography",font="Calibri 20 bold")
lf1 = LabelFrame(root, text="Open an Image")
sv = StringVar()
n_e = Entry(lf1,font="Calibri 12",width=70,textvariable=sv,state = DISABLED)
b = Button(lf1,text="Browse for an Image",command=fildia , font="Calibri 12")
f = Frame(root)
eb = Button(f,text="Encrypt",font="Calibri 17",command=en)
db = Button(f,text="Decrypt",font="Calibri 17",command=de)
lf2 = LabelFrame(root, text="Text Input or Output")
f1=Frame(lf2)
l1=Label(root,text="",font="Calibri 17")
s1=Scrollbar(f1)
e1=Text(f1,height=10,font="Calibri 13")
s1.pack(side=RIGHT,fill=Y)
e1.pack(side=LEFT,fill=BOTH)
s1.config(command=e1.yview)
e1.config(yscrollcommand=s1.set)
l.pack(padx=10,pady=7)
lf1.pack(padx=10,pady=4,fill=BOTH)
n_e.pack(side=LEFT,fill=BOTH,padx=10,pady=5)
b.pack(side=LEFT,fill=BOTH,padx=10,pady=5)
f.pack(padx=10,pady=4)
eb.pack(padx=10,pady=7,fill=BOTH,side=LEFT)
db.pack(padx=10,pady=7,fill=BOTH,side=LEFT)
f1.pack(padx=10,pady=10)
lf2.pack(padx=10,pady=10)
l1.pack(pady=7)
root.mainloop()



