import json
import os
import time

import gi
import requests

gi.require_version("Gtk", "3.0")
gi.require_version('Gdk', '3.0')
from gi.overrides import Gdk, GLib

from gi.repository import Gtk


# class to show textinput
class EntryWindow(Gtk.Window):
    def __init__(self, content):
        super().__init__(title="translate to DE")
        self.set_size_request(400, 50)
        self.connect("destroy", Gtk.main_quit)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text(content)
        self.entry.connect("activate", self.on_entry_activate)

        self.pb = Gtk.ProgressBar()
        vbox.pack_start(self.pb, True, True, 0)
        self.activity_mode = False
        self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)

        vbox.pack_start(self.entry, True, True, 0)

        self.state = False

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.activity_mode:
            self.pb.pulse()
        else:
            self.pb.set_fraction(0.0)
        return True

    def on_entry_activate(self, widget):
        if self.state:
            self.close()
        else:
            data = f"text={self.entry.get_text()}&target_lang={target}"
            self.activity_mode = True
            response = requests.post('https://api-free.deepl.com/v2/translate', headers=headers, data=data)
            # self.pb.set_fraction(0.0)
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
            self.entry.set_editable(False)
            self.state = True
            time.sleep(2)
            self.activity_mode = False


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
