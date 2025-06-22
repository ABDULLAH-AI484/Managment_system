from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from inventory import Inventory, NegativeQuantityError, NegativePriceError, ItemNotFoundError
import os
from fastapi.responses import Response
app = FastAPI()


# Setup templates and static files
from pathlib import Path
BASE_DIR = Path(__file__).parent

# Update your template config:
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory="static"), name="static")


# Initialize inventory
inventory = Inventory()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/inventory", response_class=HTMLResponse)
async def inventory_dashboard(request: Request):
    try:
        items = inventory.get_all_items()
        return templates.TemplateResponse(
            "inventory.html",
            {"request": request, "items": items}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/add", response_class=HTMLResponse)
async def add_item_form(request: Request):
    return templates.TemplateResponse("add_item.html", {"request": request})

@app.post("/items/add", response_class=HTMLResponse)
async def add_item_submit(
    request: Request,
    name: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...)
):
    try:
        item_id = inventory.add_item(name, quantity, price)
        return templates.TemplateResponse(
            "add_item.html",
            {"request": request, "success": f"Item added with ID {item_id}"}
        )
    except (NegativeQuantityError, NegativePriceError) as e:
        return templates.TemplateResponse(
            "add_item.html",
            {"request": request, "error": str(e)},
            status_code=400
        )

@app.get("/items", response_class=HTMLResponse)
async def view_items(request: Request):
    return templates.TemplateResponse(
        "view_items.html",
        {"request": request, "items": inventory.get_all_items()}
    )

@app.get("/items/remove", response_class=HTMLResponse)
async def remove_item_form(request: Request):
    return templates.TemplateResponse(
        "remove_item.html",
        {"request": request, "items": inventory.get_all_items()}
    )

@app.post("/items/remove", response_class=HTMLResponse)
async def remove_item_submit(request: Request, item_id: int = Form(...)):
    try:
        inventory.remove_item(item_id)
        return templates.TemplateResponse(
            "remove_item.html",
            {
                "request": request,
                "items": inventory.get_all_items(),
                "success": f"Item {item_id} removed successfully"
            }
        )
    except ItemNotFoundError as e:
        return templates.TemplateResponse(
            "remove_item.html",
            {
                "request": request,
                "items": inventory.get_all_items(),
                "error": str(e)
            },
            status_code=404
        )

@app.get("/items/search", response_class=HTMLResponse)
async def search_form(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/items/search", response_class=HTMLResponse)
async def search_results(request: Request, name: str = Form(...)):
    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "results": inventory.search(name),
            "search_term": name
        }
    )

@app.get("/items/low-stock", response_class=HTMLResponse)
async def low_stock_form(request: Request):
    return templates.TemplateResponse("low_stock.html", {"request": request})

@app.post("/items/low-stock", response_class=HTMLResponse)
async def low_stock_results(request: Request, threshold: int = Form(5)):
    return templates.TemplateResponse(
        "low_stock.html",
        {
            "request": request,
            "results": inventory.low_stock_alert(threshold),
            "threshold": threshold
        }
    )

# @app.get("/favicon.ico", include_in_schema=False)
# async def disable_favicon():
#     from fastapi.responses import Response
#     return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)