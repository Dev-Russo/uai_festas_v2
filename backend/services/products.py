from sqlalchemy.orm import Session
from models.user import User
from models.event import Event
from models.products import Product
from fastapi import HTTPException

def create_product(db: Session, product_data: dict, event: Event, user: User):
    # Verifica se o usuário é dono do evento
    if event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")

    payload = product_data.model_dump(exclude_none=True)

    # Cria o produto associado ao evento
    new_product = Product(**payload, event=event)
    # Adiciona e salva no banco
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    # Retorna o produto criado
    return new_product

def update_product(db: Session, product: Product, product_data: dict, event: Event, user: User):
    # Permite apenas ao dono do evento ou admin atualizar
    if event.owner.id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    # Atualiza apenas campos enviados
    payload = product_data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in payload.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    # Retorna o produto atualizado
    return product

def _collect_group_ids(db: Session, root_group_id: int) -> list:
    from models.product_group import ProductGroup
    all_groups = db.query(ProductGroup).all()
    children_map: dict = {}
    for g in all_groups:
        if g.parent_group_id is not None:
            children_map.setdefault(g.parent_group_id, []).append(g.id)
    ids = []
    stack = [root_group_id]
    while stack:
        current = stack.pop()
        ids.append(current)
        stack.extend(children_map.get(current, []))
    return ids


def get_products(db: Session, actor, event: Event):
    from models.commissioner import Commissioner
    if isinstance(actor, Commissioner):
        if actor.commissioner_group_id is None:
            return []
        from models.product_group import ProductGroupMembership
        group_ids = _collect_group_ids(db, actor.commissioner_group_id)
        product_ids = [
            pid for (pid,) in db.query(ProductGroupMembership.product_id).filter(
                ProductGroupMembership.group_id.in_(group_ids),
                ProductGroupMembership.is_active == True,
            ).all()
        ]
        return db.query(Product).filter(
            Product.event_id == event.id,
            Product.id.in_(product_ids),
        ).all()
    user = actor
    if user.role == "admin":
        db_products = db.query(Product).all()
    elif event.owner.id == user.id:
        db_products = db.query(Product).filter(Product.event_id == event.id).all()
    else:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    if not db_products:
        raise HTTPException(status_code=404, detail="Não foi encontrado os produtos")
    return db_products

def get_product_by_id(db: Session, user: User, event: Event, product_id: int):
    if user.role != "admin" and event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    
    product = db.query(Product).filter(Product.id == product_id, Product.event_id == event.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

def delete_product(db: Session, user: User, event: Event, product_id: int):
    if user.role != "admin" and event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    
    product = db.query(Product).filter(Product.id == product_id, Product.event_id == event.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(product)
    db.commit()

    return product
    
