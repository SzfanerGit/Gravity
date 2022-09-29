from gravity import create_app

app = create_app()

# Live changes for development
if __name__ == '__main__':
    app.run(debug=True)