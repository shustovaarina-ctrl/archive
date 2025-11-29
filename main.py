from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
import pet

app = FastAPI(title="Простое приложение ввода")


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


CATEGORIES = [
    {"id": 1, "name": "Грузия"},
    {"id": 2, "name": "Беларусь"},
    {"id": 3, "name": "Кыргызстан"},
    {"id": 4, "name": "Армения"},
    {"id": 5, "name": "Казахстан"},
    {"id": 6, "name": "Узбекистан"},
]


class UserInput(BaseModel):
    number: int
    category: List[str]



results = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Ввод данных",
            "categories": CATEGORIES,
            "results": results
        }
    )

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    number: int = Form(...),
    category: List[str] = Form(...),
):
    print(f"Выбранные страны: {category}")  # Для отладки
    df = pet.build_table(number, category)
    outfile = f"work_calendar_{number}.xlsx"
    df.to_excel(outfile, index=False)
    pet.apply_colors(outfile)
    print(f"Готово! Файл сохранен: {outfile}")
    # Создаем объект с введенными данными
    user_input = UserInput(
        number=number,
        category=category,

    )

    results.append(user_input)
    print(results)


    return RedirectResponse(url="/", status_code=303)

@app.post("/clear")
async def clear_results():
    global results
    results.clear()
    return RedirectResponse(url="/", status_code=303)