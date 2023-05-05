Translate Odoo PO into Chinese
===================================

Preparation:

- put PO files in `locale` folder
- set env var `OPENAI_KEY`
- add more OPENAI_KEY to `keys.json`


To **Havrest** and improve the **Quality**

- run `python main.py` to havrest your translated PO files.
- run `python qa.py` to validate the PO files, and extract the bad PO entries into One PO which used to review and correct the wrong.
- run `python cache.py` to make cache

thanks.
