# Item catalog
A web application to manage a collection of items in different categories, built with Python, Flask and SQLAlchemy

## Set up 
1. Clone this repo into your machine (local/vm)
2. In the root directory, set up and activate your virtual environment (guide [here](https://docs.python-guide.org/dev/virtualenvs/))
3. Install the dependencies using `$ pip install -r requirements.txt` from the root directory of the project
4. Run the application using `$ flask run`
5. Visit the application using your browser at <host>:5000, where <host> is the host of your machine

## Functionality
- View items in the catalog, and filter per category
- Login with your Google account using the 'login' button in the top right
- Add new items to the catalog when logged in
- Edit and delete items you created

**API**:
- Get a list of items via `/api/items`
- Get a specific item by id via `/api/item/<id>`