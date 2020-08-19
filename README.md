[![CodeFactor](https://www.codefactor.io/repository/github/alexanderivanov20/botconstructor/badge/master)](https://www.codefactor.io/repository/github/alexanderivanov20/botconstructor/overview/master)

# BotConstructor

## Formulation of the problem
A service that, through an intuitive interface and using various design patterns, allows you to configure certain parameters for the subsequent creation of a bot working program and further loading this script into the cloud platform, where the generated bot will be executed. This web application serves primarily to simplify the creation of bot program code without additional costs.

## Program description
This constructor was designed and developed in the Django framework, which, in turn, uses the MVC or MVT (Model View Controller, Model View Template) design pattern.
All files are scoped and linked.
During the implementation of this project, an algorithm was developed to form the bot program. The algorithm is based on the Facade design pattern, which allows business logic to scale to extend implementation.
After converting the configuration into a script, the service allows you to download and run the bot on the Pythonanywhere cloud platform. During the launch process, the following happens: using the Pythonanywhere API, the bot code is directly loaded, a console is created in which the program is executed.

## User manual
Upon entering the site, he is greeted with a welcome text with a small instruction, which briefly describes the actions that the user must take before starting work with this designer ...

First of all, a potential client needs to identify himself, or register, on the service, this is done in order to bind all created chatbots to a specific user in a relational database.

I logically divided the creation of a bot into several parts, more precisely into three. After registration, the user is redirected to the first step - the page where you need to specify the bot token, which can be obtained from the telegram, as well as the name and nickname, you need to keep records.

Next, the second step is the bot configuration. The client fills in the items he needs and makes a request. The request is sent via AJAX in order to speed up the response process and save traffic on hosting. All changes made are written to a JSON file. The entire filling process is protected by handlers written in advance, in order to avoid any errors from the server-side and further inaccuracies.

Step three. When you click on the NEXT button on the previous page on the backend, the following happens ... According to the developed algorithm, all configuration from a JSON file turns into a program, script, bot and is displayed in the code editor, which is built into this page. The generated code can be downloaded, or immediately uploaded to the cloud platform for hosting Python applications, Pythonanywhere and run this bot in the bash console. Also, the execution of the program can be interrupted, that is, removed from the hosting.
