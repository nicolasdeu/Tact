----
Tact
----

Short Description
=================

Tact is a program intended to help learning the art of programming for an apprentice in Computer Science. This simple application stores a Contacts list.


Goals
=====

* Learn Python
* First step in Object-oriented programming (OOP)
* Use an editor like Sublime Text
* Use a Version Control System as Git
* See the life-cycle of an application through enhancement requests and bug corrections
* Manage this life-cycle thanks to Git branches (Git Flow)
* Learn to work in a team with dedicated tools such as Trello and GitHub


Walk-through
============

Init a new project
------------------

* Start from a Python 3 project skeleton hosted on GitHub.
* Create 2 Python class: AddressBook and Contact.
* An Address Book is a list of Contacts. One will be able to append a new contact and get the number of Contacts.
* Contacts will be stored into an Address Book. A Contact will have the following attributes:

  - firstname
  - lastname
  - 1 mailing address (a string)
  - 1 phone number
  - 1 e-mailing address

* Implement a first command line which will add a Contact: *tact add [firstname] [lastname] -m [mailing address] -e [email] -p [phone number]*
* The command will return a message which indicates that contact has been added and displays all his information.






