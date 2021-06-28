import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os
import urllib
from win10toast import ToastNotifier

toaster = ToastNotifier()

root = tk.Tk()

var = tk.StringVar()
var_show = tk.StringVar()
var_entry = tk.StringVar()
var.set('下载进度：')
var_show.set('下载状态')

root.title('文件下载器')
root.attributes("-topmost", True)
root.resizable(0, 0)

label = tk.Label(root, textvariable=var)
progressbar = ttk.Progressbar(root, length=250)
root.iconbitmap("favicon.ico")
button = tk.Button(root, text='开始下载', width=15)
label_show = tk.Label(root, textvariable=var_show)
entry = tk.Entry(root, textvariable=var_entry, width=35)
label_entry = tk.Label(root, text='输入下载链接：')

label_entry.grid(row=1, column=1, pady=5, padx=5)
entry.grid(row=1, column=2)
label.grid(row=2, column=1, padx=5)
progressbar.grid(row=2, column=2, pady=5, padx=5)
button.grid(row=3, column=2, pady=5)
label_show.grid(row=3, column=1, padx=5)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


# url = 'https://download.jetbrains.com.cn/python/pycharm-professional-2021.1.2.exe'
# url = 'https://fanyiapp.cdn.bcebos.com/fanyi-client/pkg/win/1.1.2/%E7%99%BE%E5%BA%A6%E7%BF%BB%E8%AF%91_Setup_1.1.2.exe'


def check():
    url = var_entry.get()
    if url:
        file_name = urllib.parse.unquote(url.split('/')[-1])
        if file_name in os.listdir():
            var_show.set('文件已下载，不必继续下载')
        else:
            run(url, file_name)
    else:
        messagebox.showerror(title='无效的下载名称', message='请输入下载链接！')


def run(url, file_name):
    button['state'] = 'disable'
    temp = []
    var_show.set('获取文件大小...')
    num = 1
    try:
        size = int(int(requests.get(url=url, stream=True).headers['Content-Length']) / 1024 / 1024)
    except requests.exceptions.MissingSchema:
        messagebox.showerror(title='错误信息', message='请输入正确的下载链接！')
        button['state'] = 'normal'
    # var_show.set('文件大小：{}MB'.format(size))
    var_show.set('正在下载，请稍后...')
    response = requests.get(url=url, stream=True, headers=headers)
    with open(file_name, mode='ab') as file:
        for chunk in response.iter_content(chunk_size=1024):
            num += 1
            now = int(num / 1000)
            if now not in temp:
                temp.append(now)
                if now > size:
                    pass
                else:
                    print(now)
                    progressbar['value'] = ((100 * now) / size)
                    root.update()
            else:
                pass
            file.write(chunk)
    var_show.set('下载完成')
    button['state'] = 'normal'
    toaster.show_toast("下载完成",
                       "提示：{}下载已完成".format(file_name),
                       icon_path=None,
                       duration=5,
                       threaded=True)


button.config(comman=check)
root.mainloop()
