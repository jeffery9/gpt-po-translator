# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from pathlib import Path

import re
import json

json_data = "data.json"
cwd = Path(__file__).parent


if __name__ == "__main__":

    with open("%s/dictionary.json" % cwd, "r", encoding="utf8") as fp2:
        print("read dictionary data ")
        data_f = json.load(fp2)

    with open("%s/bad/bad.json" % cwd, "r", encoding="utf8") as fp3:
        print("read bad.json")
        to_del = json.load(fp3)

    with open(("%s/%s" % (cwd, json_data)), "r", encoding="utf8") as fp4:
        print("read source data.json ")
        data = json.load(fp4)
        print("merge dictionary")
        data.update(data_f)

    print(len(data))
    print(len(to_del))
    for i in to_del:
        if i in data:
            print(i)
            data.pop(i)

    print(len(data))
    with open(("%s/locale/%s" % (cwd, json_data)), "w", encoding="utf8") as file:
        print("save cache to disk")
        file.write(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=False))
