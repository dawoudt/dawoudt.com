from content_management import Content
import os
import tempfile
import shutil



TOPIC_DICT = Content()


# ORDER OF %S: "Basics" , "Basics", "Basics, "Basics"

HTML_TEMPLATE = """
{% extends "header.html" %}
{% block body %}
<!--       <pre class="prettyprint">              width="750" height="423"    -->
<body class="body">


      <div class="container" align="left" style="max-width:800px">
	  <h2>{{curTitle}}</h2>
	  <br>
	  

	  <p>{{curPost}}</p>
	  <p></p>
	  <p></p>
	  <p></p>
	  
	  
	 <!--- <kbd data-toggle="collapse" data-target="#consoleinfo" aria-expanded="false" aria-controls="consoleinfo">console</kbd>
	  
		<div class="collapse" id="consoleinfo">
		  <div class="well">
			<p class = 'alt'>When someone refers to "the console," they are referring to where information from your program is ouput. You will see an example of "output to console" below. If you want this message to go away, just click again on the "console" button that you originally clicked on.</p>
		  </div>
		</div>
		--->
		
		
		<div class="row">
			<div class="col-md-8">
				{{curCode|safe}}
		    </div>
			<div class="col-md-4">
				<p>{{curExpl}}</p>
			</div>
		</div>

		<div class = 'row'>
			<div class= 'col-md-6'>
				<p>Next post: <a title="{{nextTitle}}" href="{{nextLink}}"><button class="btn btn-primary">{{nextTitle}}</button></a></p>
				{% if prevLink%}
	  				<p><a title="back" href="{{prevLink}}"><button class="btn btn-primary">Back</button></a></p>
	  			{% endif %}
	  		</div>
	  	</div>
	</div>

	<div class = 'container-fluid'>
		<div class='row'>
			<div class = 'col-md-1'></div>
			<div class = 'col-md-11'>
				{% include 'includes/_commentbox.html' %}
			</div>
		</div>
	</div>


</body>

{% endblock %}

"""

for each_topic in TOPIC_DICT:
    print(each_topic)
    os.chdir('templates/')

    if (os.path.exists(each_topic)):
        tmp = tempfile.mktemp(dir=os.path.dirname(each_topic))
	    # Rename the dir.
        shutil.move(each_topic, tmp)
	    # And delete it.
        shutil.rmtree(tmp)
		# At this point, even if tmp is still being deleted,
		# there is no name collision.
        os.makedirs(each_topic)


    for eachele in TOPIC_DICT[each_topic]:
        try:

            filename = (eachele[1]+'.html').replace("/","")
            print(filename)
            savePath = each_topic+'/'+filename

            saveData = (HTML_TEMPLATE.replace("%s",each_topic))

            template_save = open(savePath,"w")
            template_save.write(saveData)
            template_save.close()
        except Exception as e:
            print(str(e))


	  
