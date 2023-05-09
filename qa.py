# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from pathlib import Path


import json
import re
import polib

cwd = Path(__file__).parent


bad = {}
new_po = polib.POFile()
new_po.metadata = {
    "Language": "zh_CN",
    "MIME-Version": 1.0,
    "Content-Type": "text/plain; charset=utf-8",
}


def check_occurrence(entry, pattern_list):
    match = False
    src = entry.msgid
    msgstr = entry.msgstr
    for pattern in pattern_list:
        p = re.compile(pattern)
        q_src = p.findall(src)
        q_dst = p.findall(msgstr)
        if not len(q_src) == len(q_dst):
            print("r\"%s\" mis-match" % pattern)
            match = True
            break

    return match


def check_prefix(entry, prefix_list):
    match = False
    src = entry.msgid
    msgstr = entry.msgstr
    for prefix in prefix_list:
        if src.startswith("$") and not msgstr.startswith("$"):
            print("%s mis-match" % prefix)
            match = True
            break

    return match


if __name__ == "__main__":
    top_dir = "%s/locale" % (cwd)
    for file in Path(top_dir).rglob("*.po"):
        print(file)

        po_file = polib.pofile(str(file))
        l_cnt = 0

        if "legal.po" in str(file) or "l10n_" in str(file):
            continue

        for entry in po_file:
            src = entry.msgid
            msgstr = entry.msgstr

            pattern_list = [
                "`",
                "\*",
                "\$",
                "%",
                "\{",
                "\}",
                "<div",
                "</div>",
                "<table",
                "</table>",
                "<p",
                "</p>",
                "<t ",
                "</t>",
            ]
            match = check_occurrence(entry, pattern_list)
            if match:
                bad.update({src: msgstr})
                new_po.append(entry)

            prefix_list = ["#", "+", "-", "$", "%", "\n"]

            match = check_prefix(entry, prefix_list)
            if match:
                bad.update({src: msgstr})
                new_po.append(entry)

            if len(msgstr) / len(src) > 1:
                print("excessive")
                bad.update({src: msgstr})
                new_po.append(entry)

            s_dst = re.findall(u"[\u4e00-\u9fa5]", msgstr)
            if len(s_dst) == 0 and len(src) > 16:
                # if "`" in src or "<" in src or "{" in src or "[" in src or "$" in src:
                if (
                    src.startswith(":")
                    or src.startswith("`")
                    or src.startswith("$")
                    or src.startswith("%")
                    or src.startswith("<")
                ):
                    continue
                else:
                    print("not translate")
                    bad.update({src: msgstr})
                    new_po.append(entry)

            # link = re.findall(r"(:\w+:)?(?<!`)(`[^`]+`)(?!`)", src)
            # if link:
            #     if len(src) == len(msgstr.strip()):
            #         continue

            #     else:

            #         print("found link.")
            #         bad.update({src: msgstr})
            #         new_po.append(entry)

    test_dict_list = list(bad.items())
    test_dict_list.sort(key=lambda x: len(x[0]))

    # reordering to dictionary
    res = {ele[0]: ele[1] for ele in test_dict_list}

    with open(("%s/bad/bad-1.json" % cwd), "w") as file:
        print("save to bad.json")
        print(len(res))
        file.write(json.dumps(res, indent=4, ensure_ascii=False, sort_keys=False))

    with open(("%s/bad/bad.po" % (cwd)), "w") as file:
        print("save to po file")
        file.write(str(new_po))
