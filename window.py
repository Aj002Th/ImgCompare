from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk

class app:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x150+374+182')
        self.root.title('ImgCompare')

        self.img_path1 = StringVar()
        self.img_path2 = StringVar()

        input_label1 = Label(self.root,text="图片1",font=("宋体",25),fg="black")
        input_label1.grid(row=0,column=0) 
        input_entry1 = Entry(self.root,font=("宋体",25),fg="black", textvariable=self.img_path1)
        input_entry1.grid(row=0,column=1)

        input_label2 = Label(self.root,text="图片2",font=("宋体",25),fg="black")
        input_label2.grid(row=1,column=0) 
        input_entry2 = Entry(self.root,font=("宋体",25),fg="black", textvariable=self.img_path2)
        input_entry2.grid(row=1,column=1)

        button = Button(self.root,text="比对图片",font=("宋体",25),fg="black", command=self.diff)
        button.grid(row=2,column=1)

        self.root.mainloop()
    
    def diff(self):
        print(f'input1: {self.img_path1.get()}')
        print(f'input2: {self.img_path1.get()}')
        self.show_img()
    
    def show_img(self):
        messagebox.showinfo('information', '图片比对已完成!')
        path = 'result.jpg'
        img = Image.open(path)
        img.show()

if __name__ == "__main__":
    app()