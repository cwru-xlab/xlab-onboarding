import factory

# Ref: https://stackoverflow.com/a/51397334
if __name__ == '__main__':
    factory.make_app().run()
else:
    app = factory.make_app()
