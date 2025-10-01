from fastapi import APIRouter, Depends
from sqlalchemy import func
from data.context import DBContext
from sqlalchemy.orm import Session

route_stats= APIRouter(prefix="/api/v1/stats", tags=["Stats"])
db_context = DBContext()

@route_stats.get("/overview")
async def stats_overview(db: Session = Depends(db_context.get_db)):
    total = db.query(func.count(db_context.Book.id)).scalar()

    avg = db.query(func.avg(db_context.Book.preco)).scalar()

    rating = (
        db.query(db_context.Book.rating, func.count().label("count"))
        .group_by(db_context.Book.rating)
        .all()
    )

     # Convertendo resultado de ratings para dict
    ratings_dict = {rating: count for rating, count in rating}

    return {
        "total_books": total,
        "avg_price": avg,
        "rating" : ratings_dict
    }
    
@route_stats.get("/categoria")
async def stats_categoria(db: Session = Depends(db_context.get_db)):
    result = (
        db.query(
            db_context.Book.categoria,
            db_context.Book.preco,
            func.count(db_context.Book.id).label("total")
        )
        .group_by(db_context.Book.categoria, db_context.Book.preco)
        .all()
    )

    categoria_dict = {}

    for categoria, preco, total in result:
        if categoria not in categoria_dict:
            categoria_dict[categoria] = {
                "total_livros": 0,
                "precos": {}
            }
        categoria_dict[categoria]["total_livros"] += total
        categoria_dict[categoria]["precos"][str(float(preco))] = total

    return {"categoria": categoria_dict}