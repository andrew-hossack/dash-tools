# Returns a preview of the template, used for dashtools UI
from fast_dash import FastDash
from fast_dash.Components import Text

def render():
    def text_to_text_function(input_text):
        return input_text

    app = FastDash(
        callback_fn=text_to_text_function, 
        inputs=Text, 
        outputs=Text, 
        title="FastDash Sample App",
        debug=True,
        disable_logs=True
        )
    
    return app.app.layout