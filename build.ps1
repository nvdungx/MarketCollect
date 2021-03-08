.\.venv\Scripts\Activate.ps1

pyinstaller --onedir --specpath "./" --workpath "./temp" --distpath "./build" --name MarketCollect `
--add-data="./ui/icons;./ui/icons" --add-data="./browserdriver;./browserdriver" `
--add-data="./data;./data" --paths "./src:./ui/ui_src" --icon="./ui/icons/icon-app.ico" `
--windowed --clean --noconfirm main.py

Copy-Item -Recurse -Path ".venv\Lib\site-packages\PySide6\plugins" -Destination "build\MarketCollect\PySide6"
Copy-Item -Recurse -Path ".venv\Lib\site-packages\PySide6\translations" -Destination "build\MarketCollect\PySide6"
Copy-Item -Recurse -Path ".venv\Lib\site-packages\PySide6\qt.conf" -Destination "build\MarketCollect\PySide6"