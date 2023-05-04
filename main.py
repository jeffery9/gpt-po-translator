# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import io
import itertools
import json
import os
import re
from pathlib import Path

import openai
import polib
import time

cwd = Path(__file__).parent

with open("%s/locale/data.json" % cwd, "r", encoding="utf8") as fp:
    json_data = json.load(fp)

cache = json_data

buffer = io.StringIO()
rate_limit = 3  # each key rate limit is 3 calls per minutes

key = os.getenv("OPENAI_KEY")
key_list = key.split(",")
keys = itertools.cycle(key_list)


def get_key():
    with open("%s/keys.json" % cwd, "r", encoding="utf8") as fp:
        d = json.load(fp)
        key_list.extend(d.get("keys"))

    return next(keys), 60 / rate_limit / len(key_list)


def translate_po(fn):
    po_file = polib.pofile(fn)

    for entry in po_file:
        origin_msgstr = entry.msgstr
        entry.msgstr = entry.msgid  # copy source to translation

        print("=" * 100)
        # print(entry)

        msgstr = None
        cache_key = entry.msgid
        msgstr_cached = cache.get(cache_key, None)
        if msgstr_cached:
            print("+++++++ cache hit.")
            msgstr = msgstr_cached
            print(msgstr)

        else:
            print("+++++++ cache miss.")

            key, dur = get_key()

            try:
                entry.msgstr = ""
                print(entry)
                print("+++++++ translated into... ")
                n_string = chat_completion_html(entry.msgid, key)
                print(n_string)
                print("*" * 40)
                if not n_string.startswith('msgid "'):
                    new_entry = entry
                    new_entry.msgstr = n_string
                else:
                    parser = polib._POFileParser(n_string)
                    new_entry = parser.parse()
                    new_entry = new_entry[0]

                print(new_entry)

                if new_entry:
                    if new_entry.msgstr:
                        msgstr = new_entry.msgstr
                    else:
                        msgstr = new_entry.msgid

                else:
                    msgstr = origin_msgstr

                print("waiting for the next turn ...")
                time.sleep(dur)

            except Exception as e:
                print("!" * 80)
                print(e)
                if "exceeded your current quota" in str(e):
                    print(" @@@ key suffix %s" % openai.api_key[-6:])

                if msgstr != entry.msgid:
                    msgstr = origin_msgstr

            # time.sleep(3)

        if msgstr:
            cache[cache_key] = msgstr
            # new_msgstr = ast.literal_eval(msgstr)
            new_msgstr = msgstr
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> override msgstr ")
            # print(new_msgstr)
            entry.msgstr = new_msgstr

    print("============== completed ============== %s " % fn)
    po_file.save()


def chat_completion_po(entry, key):
    try:
        message_log = [
            {
                "role": "user",
                # "content": f"You are an experienced ERP consultant proficient in both Chinese and English Please translate the MSGSTR field of the next GetText portable object entry into Chinese, and restricted to GetText portable objects are returned.",
                # "content": "You are technical translator with fluent Englis and Chinese, and a expert of odoo with the knowledge about how to localize gettext portable object",
                "content": "你是一位技术译员，精通中文和英文，并且是一位Odoo专家，熟练掌握gettext portable object翻译的技巧，非常熟悉 reStructuredText 规范和 markdown 规范，知道如何处理相关标签。",
            }
        ]
        message_log.append(
            {
                "role": "user",
                "content": "将msgstr翻译为中文，正确处理 reStructuredText 标签，返回合格的gettext portable object, 无需解释。 \n\n%s"
                % str(entry),
            }
        )

        # print(message_log)

        openai.api_key = key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301", messages=message_log, temperature=0, timeout=1
        )
        content = (
            response["choices"][0].get("message").get("content").encode("utf8").decode()
        )

        return content

    except Exception as e:
        raise e


def chat_completion_html(entry, key):
    try:
        message_log = [
            {
                "role": "system",
                # "content": f"You are an experienced ERP consultant proficient in both Chinese and English Please translate the MSGSTR field of the next GetText portable object entry into Chinese, and restricted to GetText portable objects are returned.",
                # "content": "You are technical translator with fluent Englis and Chinese, and a expert of odoo with the knowledge about how to localize gettext portable object",
                "content": "你是一位技术译员，精通中文和英文，并且是一位Odoo专家，非常熟悉 HTML规范， reStructuredText 规范，以及 markdown 规范，知道如何正确处理相关标签。",
            }
        ]
        message_log.append(
            {
                "role": "user",
                "content": f"Translate the following text to Chinese, maintaining the format and style, without providing explanations or expansions: \n\n{entry}\n ",
            }
        )

        # print(message_log)

        openai.api_key = key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301", messages=message_log, temperature=0, timeout=1
        )
        content = (
            response["choices"][0].get("message").get("content").encode("utf8").decode()
        )

        return content

    except Exception as e:
        raise e


if __name__ == "__main__":
    top_dir = "%s/locale/" % cwd
    for file in Path(top_dir).rglob("*.po"):
        print(file)
        if "l10n_" in str(file) and not "l10n_multilang" in str(file):
            continue

        translate_po(str(file))

        # save cache to data.json
        with open(("%s/data.json" % cwd), "w") as file:
            print("save to data.json")
            file.write(json.dumps(cache, indent=4, ensure_ascii=False, sort_keys=True))
