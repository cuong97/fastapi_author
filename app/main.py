from fastapi import FastAPI
from fastapi import Depends

from app.models import User
from app.routes import router as auth_router
from app.rbac.dependencies import get_current_user, require_role

app = FastAPI()
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI Auth System!"}


@app.get("/protected")
def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello {user.username}, you have access!"}


@app.get("/admin")
def admin_dashboard(user: User = Depends(require_role(["Admin"]))):
    return {"message": "Welcome Admin!"}


@app.get("/admin-user", dependencies=[Depends(require_role(["User", "Admin"]))])
def admin_dashboard():
    return {"message": "Welcome Admin and User!"}


@app.get("/user/", dependencies=[Depends(require_role(["User", "Admin"]))])
def read_user_data(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome User {current_user.username}!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
