import dash

app = dash.Dash(url_base_pathname='/sycofinder/')
#app = dash.Dash(__name__, static_folder='static')
server = app.server
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True