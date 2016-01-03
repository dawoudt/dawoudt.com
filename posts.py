
def blogExample():


    python_script_div_opening = ('<pre class="prettyprint" style="font-size: 10.5px;">'
                        '<code class="language-python">')

    python_script_div_closing = ('</code>'
                '</pre>')
                        
    python_interpreter_div_opening = ('<kbd>console</kbd>'
        '<pre style="font-size: 10.5px; color:#fff;>'
                                '<code class="language-python">'
                                "<span class='glyphicon glyphicon-info-sign' style='color:#000;'></span>"
                                    "<div class = 'well' style = 'margin: -5px 0; background-color:#000; '>")

    python_interpreter_div_closing = ('</div>'
                    '</code>'
                '</pre>')

    script = [[(python_script_div_opening+" print('Hello, World!')\n"+python_script_div_closing+
        python_interpreter_div_opening+">>> print('Hello, World!')\nHello, World!\n"+python_interpreter_div_closing)],
    [(python_script_div_opening +"\n from skelearn.datasets import load_iris\n"
        "<i> # We will be using the famous iris dataset.\n # Its noteworthy that scikit uses it's own datatype\n # called a 'Bunch' to hold dataset information</i>\n\n"
    		" from sklearn.cross_validation import train_test_split\n"
    		" from sklearn.neighbors import KNeighborsClassifier as KNC\n"
    		" from sklearn import metrics\n"
    		"\n\n"
        	" iris = load_iris()\n"
        	" X = iris.data\n"
        	" y = iris.target\n" +python_script_div_closing+

            python_interpreter_div_opening+
                " >>> X.shape\n" 
                " <strong>(150L, 4L)</strong>\n" 
                " >>> y.shape\n"
                " <strong>(150L, )</strong>"
            +python_interpreter_div_closing+
        	"\n"
            +python_script_div_opening+
        	" X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)\n"
        	" knn = KNC(n_neighbors = 5)\n"
        	" knn.fit(X_train, y_train)\n"
            +python_script_div_closing+

            python_interpreter_div_opening+
                " >>> y_pred = knn.predict(X_test)\n"
                " >>> print(metrics.accuracy_score(y_test, y_pred))\n"
                " 0.96\n"
                " >>> knn.predict([3,5,3,2])\n"
                " array([2])" 
            +python_interpreter_div_closing+
        	"\n"
        	" ")], \
        ("")]
    example = [[("Hello World!")],
    [("Prediciting Iris Species")],
    [("")]]

    return script, example


  
