**INFORMATION FOR MILESTONE 3:**

__Unit Testing:__

According to our unit testing coverage report, our unit tests cover 72% of all of our code. Running the unit tests is outlined in the "instructions" section.


__Documents:__

Sprint planning documents are located in docs/planning.
Standup documents are located in docs/StandupMeetings. 
Retrospective documents are located in docs/retrospectives.

__Instructions for Running our Project:__

Our project is built on Django. To run it, do the following:
* Clone this repository
* Navigate to the cloned repository's source directory.
* Run 'python manage.py makemigrations'
* Run 'python manage.py migrate'
* Run 'python manage.py runserver'
* If you are given Django package errors, install the specified packages to continue.
* Navigate to the URL specified in the console (Usually 127.0.0.1).
* Feel free to make a superuser for access to the /admin/ URL workspace: 'python manage.py createsuperuser'
    * You can create, modify, delete, view auction-related information at the admin control panel.
* Let us know if you run into any issues.

* Unit Testing:
    * Run 'python manage.py test'
    * If you want to see coverage report (not necessary to run the tests):
        * 'pip install coverage'
        * 'coverage run --source='.' manage.py test'
        * 'coverage report'


__Project Completion__

We estimate 85-90% of our project to be completed. At this point, we only have UI changes to make. Project functionality is basically finished.

__Documents__

The Milestone 3 Deliverables list specifies Systems Design and System Analysis documents. We were unsure if these were necessary, but we created them anyway. They exist under the docs/ directory. Additionally, we updated and finalized documents as needed for this milestone submission.


----------


An explanation of the organization and name scheme for the workspace:

    This project is going to be a silent auction. With this, up to 300 users should be able to bid on an item at a time. 

Version-control procedures:

    For version control, each issue completed will increment the current version by 0.1. A major release to deployment will increment the verion of the project by 1. So, a minor bug fix or feature will raise the project from 4.5 to 4.6 whereas a major feature will set the version from 4.6 to 5.0. Version control will also be ensured by using GitHub to ensure that changes are tracked properly.

Tool stack description and setup procedure:

    We'll be using python and django for for both the front and backend. 

Build instructions:

    To build our project, first make sure python 3 is installed and then download the project. From here, unzip or extract the project to your desired location and navigate there with a terminal to the root of the project. From the root of the project, it is neccesary to to import the databases, which can be done by typing "python manage.py migrate" followed by "python manage.py makemigrations". From here, run "python manage.py runserver" and the server should now be up and running.

Unit testing instructions:

    For unit testing, the standard library from django includes a unit testing tools and those will be used for the unit testng.

System testing instructions:

    System testing is where the whole app is run from the beginning to the end of the system. Automation would be desired, similar to Unit tests. However, most of the testing will most likely be performed by the developers as each feature is added to functionality.

Protoypes:

    There are currently three protoypes in the folder. There are the Hi, Medium and Low prototypes there. You can access as you wish, the high is a video, the medium is a powerpoint and the low is a pdf.

How to run:

    The current directories are set up and a working prototype is there. To access it, clone into the master branch and then open the html files within your browser. You can accomplish this by using file explorer and going to the location where you cloned in to master, go into the src directory, find a html file you like, and drag onto the browser.