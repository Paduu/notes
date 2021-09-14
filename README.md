# Notes APP
Create notes, report & calculate Arbeitszeit
## Setup
*Linux guide only*,
*Virtualenv recommended*

`git clone <url> && 
cd notes &&
pip install -e .`

## How to test the SQL ALchemy Models from CMD
You cannot directly load the models, if you do so, you will run into the following error:
 *RuntimeError: No application found. Either work inside a view function or push an application context*

 To circument this, we can use the shell function of Flask.
 `export FLASK_APP='notes'` - set the environment variable
 `flask shell` - start flask in shell mode
 `from notes.models import Notes` - import the respective DB module
 `Notes.query.all()` - execute querys