This is simple console application to use Zorra Telecom HLR Service

Join [Zorra Telecom](https://zorra.com/ru)

App supports import numbers for checking from __File__ (`.xlsx`, `.csv`, `.txt` supported) or directly from __console__

Executable file for Windows located in __dist/__ Folder


Steps for using app:
- run `zorra_hlr.exe`
- enter your *email* and *passowrd* on Zorra
- choose how you want to enter numbers
- then app will send requests and waiting for results (!!do not close console window till this finished)
- when app receive all results you should type Path for *output* file
- result will stored in *.csv* file named `hlr_results_{datetime}` (where `datetime` is the date and time when app was runned)

<br>

---

You also can build executable file for your OS using *pyinstaller* module in virtual enviroment:
- Clone source code to some dir
- Install __*virtualenv*__ module: `pip install virtualenv`
- Run `virtualenv venv` in application directory to create Python virtual enviroment
- Install requirments: `pip install -r requirments.txt`
- Install __*pyinstaller*__ module: `pip install pyinstaller`
- Run `pyinstaller --onefile main.py` to create executable file (it will be saved to *dist/* Folder) 


TO DO (next version):
- optimize `wait time` timeout for large files;
- change UI to Windowed (using __tkinter__);