@echo off

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Environment setup complete.
echo Activate the environment using:
echo venv\Scripts\activate

pause