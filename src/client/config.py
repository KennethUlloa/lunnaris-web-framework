from client.routes import router

def init(app):
    app.include_router(router)