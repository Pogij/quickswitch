# -*- coding: utf-8 -*-
# Copyright (C) 2012 Matevž Pogačar (matevz.pogacar@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307, USA.

import os
from gi.repository import GObject, Gdk, Gtk, Gedit, PeasGtk
from xml.etree import ElementTree



# QuickSwitchSettings represents plugin settings where user can configer quickswitch to fit hers/his needs.

class QuickSwitchSettings(Gtk.Grid):

	parent = None

	file_path = None

	default_width = 160
	default_height = 190
	default_color = "#f0f099"

	default_position_type = 1
	default_position_x = 0
	default_position_y = 0

	#Setts parent object.
	def setSettings(self, parent, file_path):
		self.parent = parent
		self.file_path = file_path


	#Creates UI for cofigurations.
	def do_create_configure_widget(self):
		widget = Gtk.Grid()

		et = ElementTree.parse(self.file_path + "config.xml")

		width = self.default_width
		height = self.default_height
		color = self.default_color

		position_type = self.default_position_type
		position_x = self.default_position_x
		position_y = self.default_position_y

		width_xml = et.find("width")
		if not width_xml == None and not width_xml.text == None:
			width = int(width_xml.text)
			if width < 150:
				width = 150
		height_xml = et.find("height")
		if not height_xml == None and not height_xml.text == None:
			height = int(height_xml.text)
			if height < 150:
				height = 150
		color_xml = et.find("color")
		if not color_xml == None and not color_xml.text == None:
			color = color_xml.text
		position_xml = et.find("position")
		position_type_xml = position_xml.find("type")
		if not position_type_xml == None and not position_type_xml.text == None:
			position_type = int(position_type_xml.text)
		position_x_xml = position_xml.find("coordinatex")
		if not position_x_xml == None and not position_x_xml.text == None:
			position_x = int(position_x_xml.text)
		position_y_xml = position_xml.find("coordinatey")
		if not position_y_xml == None and not position_y_xml.text == None:
			position_y = int(position_y_xml.text)

		label_width = Gtk.Label("Width: ")
		label_height = Gtk.Label("Height: ")
		label_color = Gtk.Label("Background color: ")
		label_position = Gtk.Label("Position: ")

		scale_width = Gtk.HScale()
		scale_height = Gtk.HScale()
		scale_width.set_digits(0)
		scale_height.set_digits(0)
		scale_width.set_range(150, 500)
		scale_height.set_range(150, 500)
		scale_width.set_name("width")
		scale_height.set_name("height")

		scale_width.set_value(width)
		scale_height.set_value(height)

		button_color = Gtk.ColorButton.new()
		button_color.set_color(Gdk.Color.parse(color)[1])
		button_color.set_name("color")

		positionBox = Gtk.VBox()
		positionBox.set_name("position")

		position1 = Gtk.RadioButton.new_with_label_from_widget(None, "Top left corner");
		position1.set_name("1")
		position1.connect("toggled", self.positioning_change, "1")
		positionBox.pack_start(position1, True, True, 0)
		position2 = Gtk.RadioButton.new_with_mnemonic_from_widget(position1, "Top right corner")
		position2.set_name("2")
		position2.connect("toggled", self.positioning_change, "1")
		positionBox.pack_start(position2, True, True, 0)
		position3 = Gtk.RadioButton.new_with_mnemonic_from_widget(position1, "Center of the screen")
		position3.set_name("3")
		position3.connect("toggled", self.positioning_change, "1")
		positionBox.pack_start(position3, True, True, 0)
		position4 = Gtk.RadioButton.new_with_mnemonic_from_widget(position1, "Custom")
		position4.set_name("4")
		position4.connect("toggled", self.positioning_change, "2")
		positionBox.pack_start(position4, True, True, 0)

		xBox = Gtk.HBox()
		xBox.set_name("boxx")
		labelx = Gtk.Label("X: ")
		xBox.pack_start(labelx, True, True, 0)
		entryx = NumberEntry()
		entryx.set_name("entryx")
		entryx.set_max_length(4)
		entryx.set_text(str(position_x))
		xBox.pack_start(entryx, True, True, 0)
		positionBox.pack_start(xBox, True, True, 0)
		
		yBox = Gtk.HBox()
		yBox.set_name("boxy")
		labely = Gtk.Label("Y: ")
		yBox.pack_start(labely, True, True, 0)
		entryy = NumberEntry()
		entryy.set_name("entryy")
		entryy.set_max_length(4)
		entryy.set_text(str(position_y))
		yBox.pack_start(entryy, True, True, 0)
		positionBox.pack_start(yBox, True, True, 0)
		

		if position_type == 2:
			position2.set_active(True)
			entryx.set_sensitive(False)
			entryy.set_sensitive(False)
		elif position_type == 3:
			position3.set_active(True)
			entryx.set_sensitive(False)
			entryy.set_sensitive(False)
		elif position_type == 4:
			position4.set_active(True)
			entryx.set_sensitive(True)
			entryy.set_sensitive(True)
		else:
			position1.set_active(True)
			entryx.set_sensitive(False)
			entryy.set_sensitive(False)

		button_reset = Gtk.Button("Reset Defaults")
		button_save = Gtk.Button("Save")
		button_reset.connect("pressed", self.reset_defaults)
		button_save.connect("pressed", self.save_settings)

		label_width.set_margin_bottom(10)
		label_height.set_margin_bottom(10)
		label_color.set_margin_bottom(10)
		label_position.set_margin_top(10)
		scale_width.set_margin_bottom(10)
		scale_height.set_margin_bottom(10)
		button_color.set_margin_bottom(10)
		button_reset.set_margin_bottom(20)
		button_reset.set_margin_top(20)
		button_save.set_margin_bottom(20)
		button_save.set_margin_top(20)

		self.attach(label_width, 0, 0, 1, 1)
		self.attach(label_height, 0, 1, 1, 1)
		self.attach(label_color, 0, 2, 1, 1)
		self.attach(label_position, 0, 3, 1, 1)
		self.attach(scale_width, 1, 0, 1, 1)
		self.attach(scale_height, 1, 1, 1, 1)
		self.attach(button_color, 1, 2, 1, 1)
		self.attach(positionBox, 1, 3, 1, 1)
		self.attach(button_reset, 0, 4, 1, 1)
		self.attach(button_save, 1, 4, 1, 1)

		return self


	#On position change.
	def positioning_change(self, widget=None, data=None):
		for child in widget.get_parent().get_children():
			if child.get_name() == "boxx" or child.get_name() == "boxy":
				if data == "2":
					for childchild in child.get_children():
						childchild.set_sensitive(True)
				else:
					for childchild in child.get_children():
						childchild.set_sensitive(False)


	#Setts hardcoded default settings.
	def reset_defaults(self, widget, data=None):
		for child in widget.get_parent().get_children():
			if child.get_name() == "width":
				child.set_value(self.default_width)
			elif child.get_name() == "height":
				child.set_value(self.default_height)
			elif child.get_name() == "color":
				child.set_color(Gdk.Color.parse(self.default_color)[1])
			elif child.get_name() == "position":
				for childchild in child.get_children():
					if childchild.get_name() == "1":
						childchild.set_active(True)


	#Saves settings to xml file.
	def save_settings(self, widget, data=None):

		new_width = self.default_width
		new_height = self.default_height
		new_color = self.default_color
		new_position_type = self.default_position_type
		new_position_x = self.default_position_x
		new_position_y = self.default_position_y

		for child in widget.get_parent().get_children():
			if child.get_name() == "width":
				new_width = child.get_value()
			elif child.get_name() == "height":
				new_height = child.get_value()
			elif child.get_name() == "color":
				new_color = child.get_color().to_string()
			elif child.get_name() == "position":
				for childchild in child.get_children():
					if childchild.get_name() == "boxx":
						for child3 in childchild.get_children():
							if child3.get_name() == "entryx":
								new_position_x = child3.get_text()
					elif childchild.get_name() == "boxy":
						for child3 in childchild.get_children():
							if child3.get_name() == "entryy":
								new_position_y = child3.get_text()
					else:
						if childchild.get_active() == True:
							new_position_type = childchild.get_name()

		et = ElementTree.parse(self.file_path + "config.xml")

		width_xml = et.find("width")
		width_xml.text = str(new_width)[:-2]
		height_xml = et.find("height")
		height_xml.text = str(new_height)[:-2]
		color_xml = et.find("color")
		color_xml.text = new_color

		position_xml = et.find("position")
		position_type_xml = position_xml.find("type")
		position_type_xml.text = new_position_type
		position_x_xml = position_xml.find("coordinatex")
		position_x_xml.text = str(int(new_position_x))
		position_y_xml = position_xml.find("coordinatey")
		position_y_xml.text = str(int(new_position_y))

		et.write(self.file_path + "config.xml")

		self.parent.setSettings(int(new_width), int(new_height), new_color, int(new_position_type), int(new_position_x), int(new_position_y))
		

#Class NumberEntry is used so text input can be limited to accept digits only.

class NumberEntry(Gtk.Entry):
    def __init__(self):
        Gtk.Entry.__init__(self)
        self.connect('changed', self.on_changed)

    def on_changed(self, *args):
        text = self.get_text().strip()
        self.set_text(''.join([i for i in text if i in '0123456789']))
