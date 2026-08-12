from fastapi import APIRouter

router = APIRouter()

@router.post("/logout")
async def logout() -> dict:
    """Logs the user out (client should delete stored tokens)."""
    return {"message": "Successfully logged out."}
