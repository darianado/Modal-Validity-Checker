LOGIC OF GOSSIP
///////////////
Modal validity checker in Python

Set up:
--------------------------------
"Modal Validity Checker" executable could not be compressed below 60MB so here are the instructions for creating it:

OPTION 1:

Requirements: python >3 and pip3
1. get pyinstaller using "pip3 install -U pyinstaller" in terminal
https://pyinstaller.org/
2. get customtkinter using "pip3 install customtkinter" in terminal
https://github.com/TomSchimansky/CustomTkinter
3. run the following command with all paths changed accordingly: 

pyinstaller --noconfirm --onefile --windowed --add-data "path/to/parse.py;." --add-data "path/to/lexer.py;." --add-data "path/to/tableau_procedure.py;." --add-data "path/to/modelGraph.py;." --hidden-import "networkx" --hidden-import "matplotlib" --add-data "C:/Users/<user_name>/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter;customtkinter/"  "path/to/main.py"

Alternatively, Auto Py to Exe could be used respecting https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging

This will generate an executable file for the modal validity checker, and by clicking it, the App is opened.

OPTION 2:

Python and pip are still required for this alternative.
Go to terminal in the project directory and run "python main.py"

If any package is not already installed, intall it using pip in the same manner as we did in option 1 with customtkinter
The packages used by the modal valitity checker are: re, copy, random, tkinter, customtkinter, networkx, matplotlib
Make sure all the necessary files are in the same folder

Author:
--------------------------------
Dariana Dorin
KCL dissertation 2023
