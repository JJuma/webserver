#Web-server
Basic HTTP web-server application which can listen on a configurable TCP port and serve both static HTML and dynamically generated HTML

#How to use
Download the zip (or run a git clone https://github.com/JJuma/Web-server.git, and make sure you have Python 3.6+ installed. Run the webserver.py to run on port 8000 or run Run the webserver.py to run on a specific port. On your browser or postman go to url http://localhost/ or http://localhost/index.html to open index.html.
You can add custom html pages in the templates folder and view them using the same process.

URL rewriting feature such as mod_rewrite in Apache. Is also included.
In the url_rewrite.ini file you can add a rewrite rule.
Currently there are 2 rules post and article written in the form:
<name> = <url regex> <result>
eg In for article the rule is as shown below:
  ^article/([^/.]+)/([^/.]+)$ article?id=$1&title=$2
  for url input http://localhost:8000/article/12/code
  will be rewritten to http://localhost:8000/article?id=12&title=code
  
    First the ^(caret) starts the expression.
    article: If anything besides "article" is typed in, the URL rewrite will not take place.
    The ([^/.]+) indicates that anything can be written between the forward slash besides the characters following the caret, in this case, the forward slash or period.
    article?id=$1&title=$2: Each value in the parentheses will be extracted and then applied to the longer URL in the substitution part of the expression. $1 indicates the first       parantheses, $2, the second. 
