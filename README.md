# Web-server
Basic HTTP web-server application which can listen on a configurable TCP port and serve both static HTML and dynamically generated HTML

# How to use
* Download the zip (or run a git clone https://github.com/JJuma/Web-server.git, and make sure you have Python 3.6+ installed. Run the webserver.py to run on port 8000 or run Run the webserver.py to run on a specific port. On your browser or postman go to url http://localhost/ or http://localhost/index.html to open index.html.
* You can add custom html pages in the templates folder and view them using the same process.

## URL rewriting
URL rewriting feature such as mod_rewrite in Apache is also included.<br />
In the url_rewrite.ini file you can add a rewrite rule.<br />
Currently there are 2 rules 'post' and 'article' written in the form:
<name> = <url regex> <result><br />
  * <url regex> is used to check if the url is a match for the rule
  * <result> is how the rewritten url will appear.
> e.g. <br /> 
> In the provided rules we have articles rule as shown below:<br />
> ^article/([^/.]+)/([^/.]+)$ article?id=$1&title=$2<br />
In which url input http://localhost:8000/article/12/code will be rewritten to http://localhost:8000/article?id=12&title=code<br />

In the 'article' rule:
* ^(caret):  starts the expression.<br />
* article:  if anything besides "article" is typed in, the URL rewrite will not take place.
* ([^/.]+):  indicates that anything can be written between the forward slash besides the characters following the caret, in this case, the forward slash or period. 
* article?id=$1&title=$2: Each value in the parentheses above will be extracted and then applied to the longer URL in the substitution part of the expression. $1 indicates the first parantheses, $2, the second.
