from main import create_app


def test_create_app_registers_user_router():
    app = create_app(None)
    routes = {route.path for route in app.routes}

    assert "/users/" in routes
    assert "/users/{user_id}" in routes
    assert "/users/email/{email}" in routes
