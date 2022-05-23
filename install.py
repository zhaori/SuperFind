import os
from threading import Thread


class Py_install(object):
    def __init__(self):
        self.package_list = [
            'fuzzywuzzy==0.18.0',
            'ttkbootstrap==1.7.6',
            # 'watchdog==2.1.5',
            'jieba==0.42.1',
            # 'pymongo==3.12.0',
            'python-Levenshtein==0.12.2',
            'redis==2.10.6',
            'pyperclip==1.8.2',
            # 'pyinstaller'
        ]
        self.install_list = [Thread(target=self.__install_page, args=(s,)) for s in self.package_list]

    @staticmethod
    def __install_page(s_name):
        os.system(f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple {s_name}')

    def install(self):
        for p in self.install_list:
            p.start()
        for i in self.install_list:
            i.join()


def upgrade_pip():
    os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip')


if __name__ == '__main__':
    upgrade_pip()
    Py_install().install()
