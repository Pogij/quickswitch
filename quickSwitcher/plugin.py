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
from dialog import QuickSwitchDialog
from settings import QuickSwitchSettings
from xml.etree import ElementTree

width = None
height = None
color = None
position_type = None
position_x = None
position_y = None

UI_XML = """<ui>
<menubar name="MenuBar">
	<menu name="ToolsMenu" action="Tools">
	  <placeholder name="ToolsOps_3">
		<menuitem name="QuickSwitchAction" action="QuickSwitchAction"/>
	  </placeholder>
	</menu>
</menubar>
</ui>"""
class QuickSwitcher(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
	__gtype_name__ = "QuickSwitcher"
	window = GObject.property(type=Gedit.Window)

	default_width = 160
	default_height = 190
	default_color = "#f0f099"

	default_position_type = 1
	default_position_x = 0
	default_position_y = 0

	dialog = None
	file_path = None
   
	def __init__(self):
		GObject.Object.__init__(self)
		self.file_path = os.path.expanduser('~') + "/.local/share/gedit/plugins/quickSwitcher/"
		et = ElementTree.parse(self.file_path + "config.xml")

		global width
		global height
		global color
		global position_type
		global position_x
		global position_y

		width = self.default_width
		height = self.default_height
		color = self.default_color
		position_type = self.default_position_type
		position_x = self.default_position_x
		position_y = self.default_position_y

		width_xml = et.find("width")
		if not width_xml == None:
			width = int(width_xml.text)
			if width < 150:
				width = 150
		height_xml = et.find("height")
		if not height_xml == None:
			height = int(height_xml.text)
			if height < 150:
				height = 150
		color_xml = et.find("color")
		if not color_xml == None:
			color = color_xml.text
		position_xml = et.find("position")
		if not position_xml == None:
			position_type_xml = position_xml.find("type")
			if not position_type_xml == None:
				position_type = int(position_type_xml.text)
				if position_type < 1 or position_type > 4:
					position_type = 1
			position_x_xml = position_xml.find("coordinatex")
			if not position_x_xml == None:
				position_x = int(position_x_xml.text)
			position_y_xml = position_xml.find("coordinatey")
			if not position_y_xml == None:
				position_y = int(position_y_xml.text)

		
	
	def _add_ui(self):
		manager = self.window.get_ui_manager()
		self._actions = Gtk.ActionGroup("QuickSwitchActions")
		self._actions.add_actions([('QuickSwitchAction', Gtk.STOCK_INFO, "Quick switch", '<Ctrl>e', "Open Quick Switch.", self.on_quick_switcher),])
		manager.insert_action_group(self._actions)
		self._ui_merge_id = manager.add_ui_from_string(UI_XML)
		manager.ensure_update()
		
	def do_activate(self):
		self._add_ui()

	def do_deactivate(self):
		self._remove_ui()

	def do_update_state(self):
		pass
		
	def _remove_ui(self):
		manager = self.window.get_ui_manager()
		manager.remove_ui(self._ui_merge_id)
		manager.remove_action_group(self._actions)
		manager.ensure_update()



	def on_quick_switcher(self, action, data=None):
		tabs = self.get_tabs()

		global width
		global height
		global color
		global position_type
		global position_x
		global position_y

		self.dialog = QuickSwitchDialog(self, tabs, width, height, color, position_type, position_x, position_y)
		self.dialog.show_all()



	def get_tabs(self):
		tabs = []
		for document in self.window.get_documents():
			tabs.append(document.get_short_name_for_display())

		return tabs
				


	def do_create_configure_widget(self):
		settingsGrid = QuickSwitchSettings()
		settingsGrid.setSettings(self, self.file_path)
		return settingsGrid.do_create_configure_widget()


	def setSettings(self, new_width, new_height, new_color, new_position_type, new_position_x, new_position_y):
		global width
		global height
		global color
		global position_type
		global position_x
		global position_y

		width = new_width
		height = new_height
		color = new_color
		position_type = new_position_type
		position_x = new_position_x
		position_y = new_position_y