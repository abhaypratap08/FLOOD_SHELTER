from flood_app import Config, create_app

app = create_app()


if __name__ == "__main__":
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.FLASK_RUN_HOST,
        port=Config.FLASK_RUN_PORT,
    )
