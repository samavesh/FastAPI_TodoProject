from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='TodoApp/templates')           # Create a Jinja2Templates instance to render HTML templates. The directory parameter specifies the location of the templates folder, which contains the HTML files used for rendering views in the application.
