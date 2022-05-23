"""
过滤json配置文件修改刷新，如果Filters.json文件下有类别有新增或删除，可以运行此脚本刷新同步everything
"""
from json import loads, dumps
from pathlib import Path


class refreshFilter(object):
    def __init__(self):
        self.filter = Path.joinpath(Path(__file__).parent.parent, "Filters.json")
        self.data = None

    def get(self):
        with open(self.filter, 'r', encoding='utf-8') as f:
            self.data = loads(f.read())

    def refresh(self):
        all_list = []
        for k in self.data.keys():
            all_list.extend(self.data[k])
        self.data["all"] = all_list
        with open(self.filter, 'w', encoding='utf-8') as f:
            f.write(dumps(self.data, indent=4, ensure_ascii=False))

    def get_data(self):
        self.get()
        return self.data


if __name__ == "__main__":
    f = refreshFilter()
    print(f.get_data()['all'])
    # f.refresh()
