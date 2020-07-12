from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Configure and build asset bundles."""
    main_style_bundle_landing = Bundle('src/less/home.less',
                               filters='less,cssmin',
                               output='dist/css/home.css',
                               extra={'rel': 'stylesheet/css'})  # Home Page Stylesheets Bundle
    main_style_bundle_app = Bundle('src/less/app.less',
                               filters='less,cssmin',
                               output='dist/css/app.css',
                               extra={'rel': 'stylesheet/css'})  # App Pages Stylesheets Bundle
    main_js_bundle = Bundle('src/js/main.js',
                            filters='jsmin',
                            output='dist/js/main.min.js')  # Main JavaScript Bundle
    
    assets.register('main_styles_landing', main_style_bundle_landing)
    assets.register('main_styles_app', main_style_bundle_app)
    assets.register('main_js', main_js_bundle)
    
    main_style_bundle_landing.build()
    main_style_bundle_app.build()
    main_js_bundle.build()
