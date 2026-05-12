"""
The simple example using declared definitions, and external static js/css.
"""

from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Colors API'
}

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
Swagger(app, config=swagger_config)


@app.route('/colors/<palette>/')
def colors(palette):
    all_colors = {
        'cmyk': ['cyan', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }

    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
