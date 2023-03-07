# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>python -m venv .venv</code>. This will then set up a a virtual python environment within the ".venv" directory.

    - Next, type <code>source .venv/bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the 'requirements.txt' file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser (http://localhost:5000 by default).


4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are :
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.


5. Testing

    * /!\ The functional tests require the Firefox web browser to be installed and the path to the [Selenium](https://selenium-python.readthedocs.io) Firefox driver to be added to the PATH environment variable. For this, from the command line :
    
        - under Linux, type <code>export PATH=$PATH:/absolute/path/to/the/cloning/directory/tests/functional</code>

        - under Windows, type <code>set PATH=%PATH%;C:\path\to\the\cloning\directory\tests\functional</code>

    * To run all tests using [Pytest framework](https://docs.pytest.org), type <code>pytest</code>

    * To run the unit, integration or functional tests only, type <code>pytest tests/unit</code>, <code>pytest tests/integration</code> or <code>pytest tests/functional</code>.
    
    * To generate the [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) report using the [pytest-cov](http://pytest-cov.rtfd.org/) Python module :
        
        - for a terminal report, type <code>pytest --cov=.</code>

        - for a HTML report, type <code>pytest --cov=. --cov-report=html</code>. You can access the report from the 'htmlcov/index.html' file.

    * To run the perfomance tests using [Locust](https://docs.locust.io), the app must be running (see above).
    
    Type <code>locust -f tests/performance/locustfile.py</code> to run the server which allows access to the Locust's web interface.
    Open http://localhost:8089, fill the host field with the app server address (http://localhost:5000 by default) and click on the 'Start swarming' button to run the tests. You can change for each run the number of users, the spawn rate and the run time.
    
    To do the same from the command line interface, type <code>locust -f tests/performance/locustfile.py --headless -u 6 -r 1 -H http://localhost:5000</code> to simulate six users with a one user started per second. Use 'CTRL+C' to interrupt.
