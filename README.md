# ListFlix

AI movie recommendations for what to watch next, when you don't know what to watch next.

<a  href="https://www.youtube.com/watch?v=n4wQlubaeMc" target="_blank">
<img  src="https://github.com/HarrisonLavins/ListFlix/blob/main/screenshots/user-selection.png?raw=true" width="500">
</a>

## Installation/Cloning the Project 

First, you will want to clone/download the code for this project using either:

1. your favorite `git` graphical user interface (GUI), or
2. by downloading the code as a `.ZIP` file, or
3. by using the command line as described below:

_Note: You will need `git` installed in order to perform these steps_

### Windows

```
> mkdir ListFlix
> cd ListFlix
> git clone https://github.com/HarrisonLavins/ListFlix.git
```

### macOSX/Linux

```
$ mkdir ListFlix
$ cd ListFlix
$ git clone https://github.com/HarrisonLavins/ListFlix.git
```

## Configuring your Python Environment

Depending on what machine you are on (Windows/macOSX/Linux), you will need to install the necessary Python libraries using one of the following methods:

1. Using Python Virtual Environments (the official recommendation by Flask)

[Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/installation/#virtual-environments)

Use the following to create the virtual environment for the app and install the necessary Python packages:

### Windows

```
> py -3 -m venv ListFlix
> ListFlix\Scripts\activate
> pip install -r requirements.txt
```

### macOSX/Linux

```
$ python3 -m venv ListFlix
$ . ListFlix/bin/activate
$ pip install -r requirements.txt
```
### MySQL Server

To run the application, you will need an active installation of MySQL Server on your machine. You can find the installer [here](https://dev.mysql.com/downloads/installer/)

When running the installer, choose the 'Developer' option. 

<img src="https://github.com/HarrisonLavins/ListFlix/blob/main/screenshots/MySQL Installer 1.PNG?raw=true" width="400">

Leave most settings on default. When configuring the server, create a user for the application to access the server with. The connection string we created inside the project is for 

user: `admin`

password: `ET_5600`

<img src="https://github.com/HarrisonLavins/ListFlix/blob/main/screenshots/MySQL Installer 2.PNG?raw=true" width="400">


### MySQL Server Components Setup

Run the following scripts from the `sqlscripts` folder in order for a full setup of the MySQL Server:

`createDB.py`

`createTABLES.py`


## Running the App

The current entrypoint of the application backend/web server is `app.py`

Run the server by running the following command in your terminal:

`python app.py`

You should see the application running in your terminal. If your browser does not open the app automatically, paste the default URL into your browser to view the home page:

`http://127.0.0.1:5000/`
