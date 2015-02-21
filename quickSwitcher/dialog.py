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



from gi.repository import GObject, Gdk, Gtk
import re


class QuickSwitchDialog(Gtk.Window):

	parent = None
	tabs = None
	tabnumbers = None

	width = None
	height = None
	color = None
	position_type = None
	position_x = None
	position_y = None

	def __init__(self, parent, openedtabs, width, height, color, position_type, position_x, position_y):
		Gtk.Window.__init__(self, title="")
		
		#Windows will not appear in the taskbar
		self.set_skip_taskbar_hint(True)

		self.parent = parent
		self.tabs = openedtabs
		self.width = width
		self.height = height
		self.color = color
		self.position_type = position_type
		self.position_x = position_x
		self.position_y = position_y
	
		#Set up dialog window.
		self.connect('key-release-event', self.on_key_release)
		self.connect('key-press-event', self.on_key_press)
		self.catch_within = parent.window
		self.catch_focus = True
		self.set_modal(False)
		self.set_transient_for(parent.window)
		self.set_decorated(False)
		self.set_resizable(True)
		self.set_border_width(2)
		self.set_size_request(self.width, self.height)

		window_position = self.parent.window.get_root_window().get_screen().get_active_window().get_root_coords(0, 0)

		posx = 0
		posy = 0

		if self.position_type == 1:
			coordinates = self.parent.window.get_active_view().translate_coordinates(self.parent.window, window_position[0], window_position[1])
			self.position_x = coordinates[0]
			self.position_y = coordinates[1]
		elif self.position_type == 2:
			coordinates = self.parent.window.get_active_view().translate_coordinates(self.parent.window, window_position[0], window_position[1])
			window_width = self.parent.window.get_root_window().get_screen().get_active_window().get_width()
			self.position_x = window_position[0] + window_width - self.width - 4
			self.position_y = coordinates[1]
		elif self.position_type == 3:
			self.set_position(Gtk.WindowPosition.CENTER)
			(self.position_x, self.position_y) = self.get_position()
		elif self.position_type == 4:
			self.move(self.position_x, self.position_y)

		self.move(self.position_x, self.position_y)

		self.vbox = Gtk.VBox(False, 2)

		#Set up text entry.
		self.entry = Gtk.Entry()
		self.entry.set_max_length(255)
		self.vbox.add(self.entry)

		#Set up treeview.
		tablist = Gtk.ListStore(GObject.TYPE_STRING)
		
		i = 0
		self.tabnumbers = []
		for tab in self.tabs:
			tablist.append((tab,))
			self.tabnumbers.append(i)
			i = i + 1

		self.treeview = Gtk.TreeView()
		self.treeview.set_model(tablist)
		self.treeview.set_headers_visible(False)
		self.treeview.set_enable_search(False)
		self.treeview.modify_bg(Gtk.StateFlags.NORMAL,Gdk.color_parse(self.color))
		self.treeview.set_margin_left(2)
		self.treeview.set_margin_right(2)
		self.treeview.set_margin_top(2)
		self.treeview.set_margin_bottom(2)

		column = Gtk.TreeViewColumn()
		cell = Gtk.CellRendererText()
		column.pack_start(cell, '1')
		column.add_attribute(cell, 'text', 0)
		self.treeview.append_column(column)

		try:
			self.treeview.set_cursor(0)
		except Exception:
			pass

		self.sw = Gtk.ScrolledWindow()
		self.sw.set_size_request(width, height - 40)

		self.sw.add(self.treeview)
		self.vbox.add(self.sw)
		self.add(self.vbox)



	#When keyboard key is pressed this function is called.
	def on_key_release(self, widget, event):
		if event.keyval == 65293:
			(model, ite) = self.treeview.get_selection().get_selected()

			selected = model.get_path(ite)
			selected = int(str(selected))

			current_tab = self.parent.window.get_active_tab()
			tabs = current_tab.get_parent().get_children()
			self.parent.window.set_active_tab(tabs[self.tabnumbers[selected]])

			self.destroy()
			return

		#If any other key is pressed
		elif not (event.keyval == 65364 or event.keyval == 65362):
			#If entry does not have focus.
			if not self.entry.has_focus():
				self.entry.grab_focus()
				self.entry.insert_text(chr(event.keyval), len(self.entry.get_text()))
				self.entry.select_region(len(self.entry.get_text()), len(self.entry.get_text()))
				
			
			entrytext = self.entry.get_text()
			indexStar = -1
			indexQmark = -1
		
			indexStar = entrytext.find('*')
			indexQmark = entrytext.find('?')

			regExp = ""
			
			#creates regular expression
			if not indexStar == -1:
				regExp = "^"+entrytext[:indexStar]+".*"+entrytext[indexStar+1:]+".*"
			elif not indexQmark == -1:
				regExp = "^"+entrytext[:indexQmark]+"."+entrytext[indexQmark+1:]+".*"
			else:
				regExp = "^"+entrytext+".*"
			
			#filters tabs
			tablist = Gtk.ListStore(GObject.TYPE_STRING)

			i = 0
			self.tabnumbers = []
			for tab in self.tabs:
				if re.match(regExp.lower(), tab.lower()):
					tablist.append((tab,))
					self.tabnumbers.append(i)
				i = i + 1
				
			self.treeview.set_model(tablist)
			self.treeview.set_cursor(0)
		

	def on_key_press(self, widget, event):
		#if Escape or Alt or Ctrl
		if (event.keyval == 65307 or event.keyval == 65513 or event.keyval == 65507):
			self.destroy()
			return
		elif self.entry.has_focus() and (event.keyval == 65364 or event.keyval == 65362):
			print "BBBBB"

	def do_focus_out_event(self, evt):
		self.destroy()


