python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

pip install pyinstaller

pyinstaller --windowed main.py

https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/

# todos

- [] Stop operations if you close the app
