from tkinter import *
from tkinter import ttk
import tkinter.filedialog as dir


class AppUI():

    def __init__(self, result):
        self.result = result
        root = Tk()
        # self.create_menu(root)
        self.create_content(root)
        # self.path = 'C:'
        root.title("数据导入工具")
        root.geometry('500x300')
        root.geometry('+40+15')
        root.resizable(False, False)  # 调用方法会禁止根窗体改变大小
        # 以下方法用来计算并设置窗体显示时，在屏幕中心居中
        curWidth = root.winfo_width()  # get current width
        curHeight = root.winfo_height()  # get current height
        scnWidth, scnHeight = root.maxsize()  # get screen width and height
        tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
        print(tmpcnf)
        root.update()
        root.mainloop()

    def create_content(self, root):
        lf = ttk.LabelFrame(root, text="数据导入")
        lf.pack(fill=X, padx=15, pady=8)

        top_frame = Frame(lf)
        top_frame.pack(fill=Y, expand=YES, side=TOP, padx=15, pady=8)

        self.search_key = StringVar()
        # ttk.Entry(top_frame, textvariable=self.search_key, width=50).pack(fill=X, expand=YES, side=LEFT)
        ttk.Button(top_frame, text="确定", command=self.search_file).pack(padx=15, fill=X, expand=YES, side=LEFT)
        ttk.Button(top_frame, text="取消", command=self.search_file).pack(padx=15, fill=X, expand=NO)

        bottom_frame = Frame(lf)
        bottom_frame.pack(fill=BOTH, expand=YES, side=TOP, padx=15, pady=8)

        band = Frame(bottom_frame)
        band.pack(fill=BOTH, expand=YES, side=TOP)

        self.list_val = StringVar()
        listbox = Listbox(band, listvariable=self.list_val, height=18)
        listbox.pack(side=LEFT, fill=X, expand=YES)

        vertical_bar = ttk.Scrollbar(band, orient=VERTICAL, command=listbox.yview)
        vertical_bar.pack(side=RIGHT, fill=Y)
        listbox['yscrollcommand'] = vertical_bar.set

        horizontal_bar = ttk.Scrollbar(bottom_frame, orient=HORIZONTAL, command=listbox.xview)
        horizontal_bar.pack(side=BOTTOM, fill=X)
        listbox['xscrollcommand'] = horizontal_bar.set

        # 给list动态设置数据，set方法传入一个元组，注意此处是设置，不是插入数据，此方法调用后，list之前的数据会被清除
        self.list_val.set(self.result)

    def search_file(self):
        pass

    def open_dir(self):
        d = dir.Directory()
        self.path = d.show(initialdir=self.path)


if __name__ == "__main__":
    AppUI('adfadfa')
