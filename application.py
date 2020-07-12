from application import create_app

application = create_app()

if __name__ == "__main__":
    application.run(host='clustify.co', port=8080, debug=True)
