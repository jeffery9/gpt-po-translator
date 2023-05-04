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
proj = "doc16"

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

            # pattern = re.compile("`")
            # q_src = pattern.findall(src)
            # q_dst = pattern.findall(msgstr)
            # if len(q_src) > len(q_dst):
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("\*")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if len(s_src) > len(s_dst):
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("<div ")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if not len(s_src) == len(s_dst):
            #     print("<div mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("</div>")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if not len(s_src) == len(s_dst):
            #     print("</div> mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("<table ")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if not len(s_src) == len(s_dst):
            #     print("<table mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("</table>")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if not len(s_src) == len(s_dst):
            #     print("</table> mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("<p ")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if not len(s_src) == len(s_dst):
            #     print("<p mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # pattern = re.compile("</p>")
            # s_src = pattern.findall(src)
            # s_dst = pattern.findall(msgstr)
            # if not len(s_src) == len(s_dst):
            #     print("</p> mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # if src.startswith("#") and not msgstr.startswith("#"):
            #     print("# mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # if src.startswith("+") and not msgstr.startswith("+"):
            #     print("+ mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # if src.startswith("-") and not msgstr.startswith("-"):
            #     print("- mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # if src.startswith("$") and not msgstr.startswith("$"):
            #     print("$ mis-match")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # if len(msgstr) / len(src) > 1:
            #     print("excessive")
            #     bad.update({src: msgstr})
            #     new_po.append(entry)

            # s_dst = re.findall(u"[\u4e00-\u9fa5]", msgstr)
            # if len(s_dst) == 0 and len(src) > 16:
            #     # if "`" in src or "<" in src or "{" in src or "[" in src or "$" in src:
            #     if  src.startswith(':') or src.startswith('`') or src.startswith('$' )or src.startswith('%') or src.startswith('<'):
            #         continue
            #     else:
            #         print("not translate")
            #         bad.update({src: msgstr})
            #         new_po.append(entry)

            link = re.findall(r"(:\w+:)?(?<!`)(`[^`]+`)(?!`)", src)
            if link:
                if len(src) == len(msgstr.strip()):
                    continue

                else:

                    print("found link.")
                    bad.update({src: msgstr})
                    new_po.append(entry)

    # test_dict_list = list(bad.items())
    # test_dict_list.sort(key=lambda x: len(x[0]))

    # # reordering to dictionary
    # res = {ele[0]: ele[1] for ele in test_dict_list}

    with open(("%s/bad/bad-1.json" % cwd), "w") as file:
        print("save to bad.json")
        print(len(bad))
        file.write(json.dumps(bad, indent=4, ensure_ascii=False, sort_keys=True))

    with open(("%s/bad/bad.po" % (cwd)), "w") as file:
        print("save to po file")
        file.write(str(new_po))
