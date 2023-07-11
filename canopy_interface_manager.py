import sublime

class CanopyInterfaceManager:

  @classmethod
  def get_cursor_position(self):
    return sublime.active_window().active_view().sel()[0].begin()

  @classmethod
  def get_selection_range(self):
    view = sublime.active_window().active_view()
    return [view.sel()[0].begin(), view.sel()[0].end()]

  @classmethod
  def set_cursor_position(self, new_position):
    view = sublime.active_window().active_view()
    view.sel().clear()
    view.sel().add(new_position)
    view.show(view.sel())

  @classmethod
  def create_quick_panel(self, collection, callback):
    sublime.active_window().show_quick_panel(
      collection, callback
    )
