from datetime import date
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class WeatherWindow(Gtk.Window):
    main_grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
    morning_grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
    morning_grid_child = Gtk.Grid()
    afternoon_grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
    afternoon_grid_child = Gtk.Grid()

    def __init__(self):
        Gtk.Window.__init__(self, title="Weather Forecast")
        self.main_grid.add(self.morning_grid)
        self.main_grid.add(self.afternoon_grid)
        self.add(self.main_grid)

        for i in range(2):
            # current date
            vbox_infos_icon = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                      spacing=10)
            label = Gtk.Label(label="{}".format("Icon"))
            label.set_markup("<span size='16000'>{}</span>".format("Icon"))
            vbox_infos_icon.pack_start(label, True, True, 0)

            vbox_infos_hour = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                      spacing=10)
            label = Gtk.Label(label="{}".format("Hour"))
            label.set_markup("<span size='16000'>{}</span>".format("Hour"))

            vbox_infos_hour.pack_start(label, True, True, 0)

            vbox_infos_temp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                      spacing=10)
            label = Gtk.Label(label="{}".format("Temp"))
            label.set_markup("<span size='16000'>{}</span>".format("Temp"))

            vbox_infos_temp.pack_start(label, True, True, 0)

            vbox_infos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                 spacing=10)
            vbox_infos.pack_start(label, True, True, 0)
            vbox_infos.add(vbox_infos_hour)
            vbox_infos.add(vbox_infos_icon)
            vbox_infos.add(vbox_infos_temp)
            if i == 0:
                today = date.today()
                app_title = Gtk.Label()
                app_title.set_markup(
                    "<span size='18000'>\n{} Forecast\n</span>".format(
                        today.strftime("%B %d, %Y")))
                title = Gtk.Label()
                title.set_markup(
                    "<span size='16000'>Morning Forecast\n</span>")
                self.morning_grid.add(app_title)
                self.morning_grid.add(title)
                self.morning_grid_child.add(vbox_infos)
            else:
                title = Gtk.Label()
                title.set_markup(
                    "<span size='16000'>\nAfternoon Forecast\n</span>")
                self.afternoon_grid.add(title)
                self.afternoon_grid_child.add(vbox_infos)

    def display(self, forecast, hour, icon, temp):

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="{}h".format(str(hour + 1)))
        vbox.pack_start(label, True, True, 0)

        vbox_icon = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="{}".format(icon))
        label.set_markup("<span size='24000'>{}</span>".format(icon))
        vbox_icon.pack_start(label, True, True, 0)

        vbox_temp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="{}".format(str(temp)))
        vbox_temp.pack_start(label, True, True, 0)

        vbox_final = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_final.add(vbox)
        vbox_final.add(vbox_icon)
        vbox_final.add(vbox_temp)
        vbox_final.set_size_request(70, 100)
        vbox_final.pack_start(label, True, True, 0)

        if hour < 12:
            self.morning_grid_child.add(vbox_final)
            self.morning_grid.add(self.morning_grid_child)
        else:
            self.afternoon_grid_child.add(vbox_final)
            self.afternoon_grid.add(self.afternoon_grid_child)
