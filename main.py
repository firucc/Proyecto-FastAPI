from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import psycopg2
import os
 
 
class Item(BaseModel):
    autor: str
    descripcion: str
    fecha_estreno: date
 
 
db_params = {
    'host': os.getenv("POSTGRES_HOST"),
    'database': os.getenv("POSTGRES_DB"),
    'user': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD"),
    'port': os.getenv("POSTGRES_PORT")
}
 
conn = psycopg2.connect(**db_params)
 
app = FastAPI()
 
@app.get("/movies")
def read_items():
    cur = conn.cursor()
    cur.execute("SELECT * FROM my_movies")
    rows = cur.fetchall()
    cur.close()
    return {"items": rows}

 
@app.post("/movies")
def create_items(item: Item):
    cur = conn.cursor()
    cur.execute("INSERT INTO my_movies (autor, descripcion, fecha_estreno) VALUES (%s, %s, %s)", (item.autor, item.descripcion, item.fecha_estreno))
    conn.commit()
    cur.close()
    return {"item": item}
 
@app.put("/movies/{movie_id}")
def put_item(movie_id: int, item: Item):
    cur = conn.cursor()
    cur.execute("UPDATE my_movies SET autor = %s, descripcion = %s, fecha_estreno = %s WHERE id = %s", (item.autor, item.descripcion, item.fecha_estreno, movie_id))
    conn.commit()
    cur.close()
    return {"item": item}
 
@app.delete("/movies/{movie_id}")
def delete_item(movie_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM my_movies WHERE id = %s", (movie_id,))
    conn.commit()
    cur.close()
    return {"item_id": movie_id}