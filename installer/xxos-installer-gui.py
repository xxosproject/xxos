#!/usr/bin/env python3
import gi, os, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
class InstallerWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='XXOS First-Time Setup (BETA)')
        self.set_default_size(520, 360)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=12)
        self.add(box)
        self.user_entry = Gtk.Entry(); self.user_entry.set_text('xxosadmin')
        self.pass_entry = Gtk.Entry(); self.pass_entry.set_visibility(False)
        self.pass_confirm = Gtk.Entry(); self.pass_confirm.set_visibility(False)
        box.pack_start(Gtk.Label(label='Web Console Admin Username:'), False, False, 0)
        box.pack_start(self.user_entry, False, False, 0)
        box.pack_start(Gtk.Label(label='Password:'), False, False, 0)
        box.pack_start(self.pass_entry, False, False, 0)
        box.pack_start(Gtk.Label(label='Confirm Password:'), False, False, 0)
        box.pack_start(self.pass_confirm, False, False, 0)
        self.host_entry = Gtk.Entry(); self.host_entry.set_text('xxos')
        box.pack_start(Gtk.Label(label='Hostname:'), False, False, 0)
        box.pack_start(self.host_entry, False, False, 0)
        self.tele_check = Gtk.CheckButton(label='Enable anonymous telemetry to xxos.org (opt-in)')
        self.remote_check = Gtk.CheckButton(label='Allow Web Console remote access from LAN (can be changed later)')
        box.pack_start(self.tele_check, False, False, 0)
        box.pack_start(self.remote_check, False, False, 0)
        btn_box = Gtk.Box(spacing=6)
        apply_btn = Gtk.Button(label='Apply & Finish'); apply_btn.connect('clicked', self.on_apply)
        cancel_btn = Gtk.Button(label='Cancel'); cancel_btn.connect('clicked', self.on_cancel)
        btn_box.pack_end(cancel_btn, False, False, 0); btn_box.pack_end(apply_btn, False, False, 0)
        box.pack_end(btn_box, False, False, 0)
    def on_apply(self, widget):
        p1 = self.pass_entry.get_text(); p2 = self.pass_confirm.get_text()
        if p1 != p2 or not p1:
            dlg = Gtk.MessageDialog(parent=self, flags=0, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format='Passwords do not match or empty.'); dlg.run(); dlg.destroy(); return
        os.makedirs('/var/lib/xxos', exist_ok=True); os.makedirs('/etc/xxos', exist_ok=True)
        with open('/var/lib/xxos/webconsole_admin_pass','w') as f: f.write(p1); os.chmod('/var/lib/xxos/webconsole_admin_pass',0o600)
        if self.tele_check.get_active(): open('/etc/xxos/telemetry-enabled','w').close()
        else:
            try: os.remove('/etc/xxos/telemetry-enabled')
            except: pass
        if self.remote_check.get_active(): open('/etc/xxos/allow-remote-console','w').close()
        else:
            try: os.remove('/etc/xxos/allow-remote-console')
            except: pass
        os.system(f'hostnamectl set-hostname {self.host_entry.get_text().strip() or "xxos"}')
        dlg = Gtk.MessageDialog(parent=self, flags=0, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, message_format='Settings saved. Reboot to apply changes.'); dlg.run(); dlg.destroy(); Gtk.main_quit()
    def on_cancel(self, widget): Gtk.main_quit()
if __name__=='__main__':
    if os.geteuid()!=0: print('Run as root'); sys.exit(1)
    win=InstallerWindow(); win.connect('destroy', Gtk.main_quit); win.show_all(); Gtk.main()
