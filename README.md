## Example functionality when using TIA Openness with Python

Basic "hello world": https://github.com/Maroder1/TIA-openness

The repo consists of two versions: one normal python file (.py) and one jupyter notebook file (.ipynb). It is strongly recommended to use jupyter when developing an openness application, as you do not have to rerunn your entire code each time you are testing and exploring.

**Note:** this is not "production code", but code to demonstrate the API. For production you should use more methods, loops and checks (partly demonstrated)

**The following topics are demonstrated.**

- Starting TIA
- Creating project
- Adding HW
- Adding IO
- Setting IP
- Creating network
- Creating IO system
- Compiling
- Exporting blocks and Tag tables
- Importing blocks and Tag tables
- Saving, closing dispoing


**NOTE: I failed to install pythonnet on python 3.8, use 3.7 if you run into problems**


**Installation of TIA Openness**

 1. Install TIA v16 professional, make sure openness is checked [default]
	[Link to TIA v16 trail](https://support.industry.siemens.com/cs/ww/en/view/109772803)
 2. Right clik "My computer" -> Manage -> System tools -> Local users and groups - > Groups-> Double click “Siemens TIA Openness” and add your username
 3. Edit the file path in the example file to match your installation of Siemens.Engineering.dll
 4. [Download and install Python](www.python.org)   (note 3.7 )


**Option 1, running directly (not recommended)**

 1. in the windows search bar type "command prompt" to open Command Promt (CMD)
 2. Install pythonnet by typing: *pip install pythonnet* (note, python 3.7)
 3. Browse to the location of the example file and type: *Python Openness_examples_python.py*


**Option 2 (recommended), running in a Virtual environment(in this example using Miniconda (Anaconda))**

 1. [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)
 2. Open Command Prompt (CMD)
 
 3. Create a new environment by typing: *conda create --name opennesspy python=3.7* (note 3.7 )
 4. Actiavte the environment: *conda activate opennesspy*
 5. Install pythonnet by typing: *pip install pythonnet*  Note: installing using *conda install* didnt work.
 6. Browse to the location of the example file and type: *Python Openness_examples_python.py*
 7. To leave the environment type *conda deactiave opennesspy*
 
 Optional: instead of manually installing use the provided environment.yml file
 
 
**Strongly Recommended: develop using Jupyter Notebook**

 1. Start Command Promt (CMD) as **administrator** (right click). Do not enter any environment yet.
 2. Install Jupyter (and nb_conda as well as ipykernel to get your environments listed: *conda install jupyter nb_conda ipykernel*
 3. Activate the environment you want to add to jupyter kernel:  *conda activate myenv*
 4. Install ipykernel in the environment (do this for all envvironemnts you would like to add):  *conda install ipykernel*
 5. To start Jupyter, cd to root (cd .. until you are at C:) then type (does not need to be inside and env): *Jupyter noteboook*
 6. You might need to confrim that it shall open in a web browser (I use chrome)
 7. Once open in a browser navigate to the folder of your choice, then make a new python 3 file.
 8. Once inside click Kernel ->  Change kernel and select the conda env you would like 
 9. To run a cell: either use the run button, or shift + enter.

 
