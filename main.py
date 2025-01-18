from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector


#MAIN
app = FastAPI()

conexion = mysql.connector.connect(user='manga', password='mangapwd',
                                   host='localhost',
                                   database='manga',
                                   port='3306')





#Base model garantiza la validacion de dartos
class Manga(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

@app.get("/")
def index():
    return {"message" : "Mi API de mangas"}


@app.get("/Manga/{id}")
def mostrar_manga(id : int):
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM mangas WHERE id =%s"
    val = (id, )

    try:
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result :
            return result
        else:
            raise HTTPException(status_code=404, detail="Manga no encontrado")
    except mysql.connector.Error as err:
        print(f"Error en la consulta: {err}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    finally:
            cursor.close()


@app.post("/mangas")
def insertar_manga(manga: Manga):
    cursor = conexion.cursor(dictionary=True)

    sql = "INSERT INTO mangas (titulo, autor, paginas) VALUES(%s, %s, %s)"
    val =(manga.titulo, manga.autor, manga.paginas)
    try:
        cursor.execute(sql, val)
        conexion.commit()
        return {"message": f"manga {manga.titulo} insertado con id {cursor.lastrowid}"}
    except mysql.connector.Error as err:
        conexion.rollback
        raise HTTPException(status_code=500, detail=f"Error al insertar manga: {err}")
    finally:
            cursor.close()
    

