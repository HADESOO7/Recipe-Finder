import os
curr_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(curr_dir, 'venv', 'Scripts')
if hasattr(os, 'add_dll_directory') and os.path.exists(scripts_dir):
    os.add_dll_directory(scripts_dir)

from Foodimg2Ing import app

if __name__=='__main__':
    app.run(debug=True)