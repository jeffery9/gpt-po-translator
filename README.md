Translate Odoo PO into Chinese
===================================

Preparation:

- put PO files in `locale` folder, or run `tx pull -l <lang_code>`, eg: zh_CN, zh_TW
<!-- - set env var `OPENAI_KEY` -->
- add OPENAI_KEY to `keys.json`, add more list item if has more OPENAI_KEY.


To **Havrest** and improve the **Quality**

- run `python main.py` to havrest your translated PO files.
- run `python qa.py` to validate the PO files, and extract the bad PO entries into One PO which used to review and correct the wrong.
- run `python cache.py` to make cache to speed up the translation process.

thanks.
