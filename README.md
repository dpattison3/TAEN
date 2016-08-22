# TAEN

This is a repository for a basic web application project. The idea and designs came from a friend. It is designed to assist small-time music artists connect and collaborate on projects.

It is set up with all neccessary for hosting on AWS and has been tested their using their elastic beanstalk cli. 

The project can also be run locally.
Requirements:
    environment variable for the Djang secret key (used for cookies/sessions)
    postgres database - specifics are in TAEN/settings.py
    Python virtual environment with all dependencies from requirements.txt installed

Basic functionality is a social media-esque site where users can be login/register and view other user profiles sorted by distance. User profiles contain various information including a profile picture, links to their work, completed projects, and tools owned.
