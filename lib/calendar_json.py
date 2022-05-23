import json
import os


class fileJSON(object):
    # noinspection PyPep8Naming
    def __init__(self):
        data_json = {
            "begin": '',
            "end": ''

        }

        self.json_file = "time.json"
        if os.path.isfile(self.json_file) is False:
            with open(self.json_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data_json, indent=4, ensure_ascii=False))

    def upgrade_value(self, root, value):
        """
        root: 预更改的键
        value：预更改的值
        """
        if os.path.isfile(self.json_file) is True:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                data_json = dict(json.loads(f.read()))
            data_json[root] = value
            with open(self.json_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data_json, indent=4, ensure_ascii=False))

    def read_time(self, root):
        if os.path.isfile(self.json_file) is True:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                data_json = dict(json.loads(f.read()))
        return data_json[root]


def create_json(key, value):
    fileJSON().upgrade_value(key, value)


if __name__ == "__main__":
    create_json('begin', '123')
    create_json('end', ' ')
