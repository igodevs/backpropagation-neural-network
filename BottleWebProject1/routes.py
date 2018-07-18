"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, static_file, run
from datetime import datetime
from zadanie import zavolaj_funkciu
from bottle import static_file
import os


@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )



@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/result', method = 'POST')
@view('result')
def result():
    """Renders the about page."""
    
    n_first_hidden = request.forms.get("first_hidden")
    n_second_hidden = request.forms.get("second_hidden")
    n_iteration = request.forms.get("iteration")

  

    #file upload
    dataset = request.files.get('csv_file') 
    save_path = "static/csv"
    file_path = "{path}/{file}".format(path=save_path, file=dataset.filename)

    if not os.path.exists(file_path):
        dataset.save(file_path)

    zavolaj_funkciu(n_first_hidden,n_second_hidden, n_iteration, file_path)

    return dict(
        title= 'Vykreslena chyba',
        
        
        year=datetime.now().year
    )


#def send_image(filename):
 #   return static_file(filename, root='Users\igor\source\repos\BottleWebProject1\BottleWebProject1', mimetype='image/png')