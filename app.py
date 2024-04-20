from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image
from compare import compare

class app:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x200+374+182')
        self.root.title('ImgCompare')

        self.img_path1 = StringVar()
        self.img_path2 = StringVar()

        Label(self.root,text="图片1",font=("宋体",25),fg="black").grid(row=0,column=0) 
        Entry(self.root,font=("宋体",25),fg="black", textvariable=self.img_path1).grid(row=0,column=1)
        Button(self.root,text="路径选择",font=("宋体",25),fg="black", command=self.select_path_img1).grid(row=0,column=2)

        Label(self.root,text="图片2",font=("宋体",25),fg="black").grid(row=1,column=0) 
        Entry(self.root,font=("宋体",25),fg="black", textvariable=self.img_path2).grid(row=1,column=1)
        Button(self.root,text="路径选择",font=("宋体",25),fg="black", command=self.select_path_img2).grid(row=1,column=2)

        Button(self.root,text="比对图片",font=("宋体",25),fg="black", command=self.diff).grid(row=2,column=1)

        self.root.mainloop()
    
    def diff(self):
        print(f'input1: {self.img_path1.get()}')
        print(f'input2: {self.img_path2.get()}')
        self.path = './'
        messagebox.showinfo('information', '图片比对即将开始!')
        compare(self.img_path1.get(), self.img_path2.get(), self.path)
        self.path = './result.jpg'
        self.show_img()
    
    def show_img(self):
        messagebox.showinfo('information', '图片比对已完成!')
        img = Image.open(self.path)
        img.show()
        self.img_path1.set('')
        self.img_path2.set('')
    
    def select_path_img1(self):
        path_ = filedialog.askopenfilename()
        #通过replace函数替换绝对文件地址中的/来使文件可被程序读取 
        #注意：\\转义后为\，所以\\\\转义后为\\
        path_=path_.replace("/","\\\\")
        self.img_path1.set(path_)

    def select_path_img2(self):
        path_ = filedialog.askopenfilename()
        path_=path_.replace("/","\\\\")
        self.img_path2.set(path_)

if __name__ == "__main__":
    app()