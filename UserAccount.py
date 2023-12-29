"""from kivymd.uix.filemanager import MDFileManager
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
    callback_function(path)"""

from flask import Flask, request, jsonify
app = Flask(__name__)

central_database = []

@app.route('/sync', methods=['POST'])
def sync_data():
    try:
        local_changes = request.get_json()
        central_database.extend(local_changes)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
