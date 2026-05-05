from fastapi import FastAPI

from yatharth_os.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Yatharth OS API",
        description="CLI-first, API-backed engineering portfolio for Yatharth Sant.",
        version="0.1.0",
    )
    app.include_router(router)
    return app


app = create_app()
