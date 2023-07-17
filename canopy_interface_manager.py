import sublime

class CanopyInterfaceManager:

  @classmethod
  def view(self):
    return sublime.active_window().active_view()

  @classmethod
  def file_length(self):
    return self.view().size()

  @classmethod
  def get_cursor_position(self):
    return self.view().sel()[0].begin()

  @classmethod
  def get_selection_range(self):
    view = self.view()
    return [view.sel()[0].begin(), view.sel()[0].end()]

  @classmethod
  def set_cursor_position(self, new_position):
    view = self.view()
    view.sel().clear()
    view.sel().add(new_position)
    view.show(view.sel())

  @classmethod
  def create_quick_panel(self, collection, callback, *index):
    sublime.active_window().show_quick_panel(
      collection, callback, selected_index=(index or 0)
    )

  @classmethod
  def insert(self, message):
    position = self.view().sel()[0].begin()
    self.view().sel().clear()
    self.view().sel().add(position)
    self.view().show(self.view().sel())
    self.view().run_command("insert", {"characters": message})
