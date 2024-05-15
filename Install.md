## Installation Instructions
1) Install HDXWizard - In the main folder of HDXWizard, click the green "<> code" button in the upper right, and download the zip file. Unzip the folder and move the folder to desired place.
2) Install Python - Go to the python website and install python 3.11. During the download, check the checkbutton that says "Add python to PATH"
3) Install Packages - Right click on HDXWizard folder and click "Copy as path". Open the command prompt (windows) or terminal (mac). Type in: **cd _copied_path_** , and click enter. Type **pip install -r requirements.txt** and click enter again
4) Create desktop shortcut (Optional) - Open any text editor, such as notepad. Write:


   **@echo off**
   
   **cd /d _copied_path_**
   
   **python hdxwizard.py**
   
   **pause**


   Save the file as a .bat file. This file will run the HDXWizard code when opened.
   
   A desktop shortcut can be created for the .bat file. An icon is available to use (WizardIcon.ico) for the shortcut (right click on shortcut > properties > change icon > browse)

   If at any point you move the HDXWizard folder, you will need to redirect the .bat file to it
