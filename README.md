# BotConstructor

A service that, through an intuitive interface and using various design patterns, allows you to configure certain parameters for the subsequent creation of a bot working program and further loading this script into the cloud platform, where the generated bot will be executed. This web application serves primarily to simplify the creation of bot program code without additional costs.

This constructor was designed and developed in the Django framework, which, in turn, uses the MVC or MVT (Model View Controller, Model View Template) design pattern.
All files are scoped and linked.
During the implementation of this project, an algorithm was developed to form the bot program. The algorithm is based on the Facade design pattern, which allows business logic to scale to extend implementation.
After converting the configuration into a script, the service allows you to download and run the bot on the Pythonanywhere cloud platform. During the launch process, the following happens: using the Pythonanywhere API, the bot code is directly loaded, a console is created in which the program is executed.
