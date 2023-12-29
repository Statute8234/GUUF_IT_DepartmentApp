from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar

def show_file_chooser(callback_function):
    file_manager = MDFileManager(
        exit_manager=lambda *args: exit_manager(file_manager),
        select_path=lambda path: select_path(file_manager, path, callback_function),
        preview=True,
    )
    file_manager.show('/')

def exit_manager(file_manager):
    file_manager.close()

def select_path(file_manager, path, callback_function):
    exit_manager(file_manager)
    Snackbar(text=path).show()
    callback_function(path)
