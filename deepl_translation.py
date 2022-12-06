import json
import os
import requests
import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Gdk', '3.0')
from gi.overrides import Gdk

from gi.repository import Gtk


# class to show textinput
class EntryWindow(Gtk.Window):
    def __init__(self, content):
        super().__init__(title="translate to DE")
        self.set_size_request(400, 70)
        self.connect("destroy", Gtk.main_quit)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text(content)
        self.entry.connect("activate", self.on_entry_activate)
        vbox.pack_start(self.entry, True, True, 0)

        self.state = 0

    def on_entry_activate(self, widget):
        if self.state:
            self.destroy()
        else:
            data = f"text={self.entry.get_text()}&target_lang={target}"
            response = requests.post('https://api-free.deepl.com/v2/translate', headers=headers, data=data)
            b = json.loads(response.text)
            print(b)
            language = "unknown"
            text = ""
            try:
                language = b["translations"][0].get("detected_source_language")
            except Exception as e:
                print(e)
            try:
                text = b["translations"][0].get("text")
            except Exception as e:
                print(e)

            print(language)
            self.entry.set_text(text)
            self.state += 1


if __name__ == "__main__":
    target = "DE"
    with open(f"{os.path.split(__file__)[0]}/auth.txt", "r") as f:
        auth = f.readline()

    headers = {
        'Authorization': f'DeepL-Auth-Key {auth}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # 1.clipboard
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    text = clipboard.wait_for_text()

    # 2. aufrufen des Programms mit der Zwischenablage
    # 3a + 3b
    ew = EntryWindow(text)
    ew.show_all()

    Gtk.main()
