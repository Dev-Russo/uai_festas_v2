from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.models.user import User
from backend.models.event import Event
from fastapi import HTTPException


def create_event(db: Session, event_data: dict, user: User):
    # Importa o model Event
    from backend.models.event import Event
    # Cria um novo evento associando ao usuário
    new_event = Event(**event_data.model_dump(), owner=user)
    # Adiciona o evento à sessão do banco
    db.add(new_event)
    # Salva no banco
    db.commit()
    # Atualiza o objeto com dados do banco
    db.refresh(new_event)
    # Retorna o evento criado
    return new_event

def update_event(db: Session, event: Event, user: User, event_data: dict):
    # Atualiza os campos do evento com os dados recebidos
    for key, value in event_data.model_dump(exclude_unset=True).items():
        setattr(event, key, value)
    # Se não for admin, só pode atualizar se for o dono
    if user.role != "admin" and user.id != event.owner.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    # Salva alterações
    db.commit()
    db.refresh(event)
    # Retorna o evento atualizado
    return event

def get_events(db: Session, user: User):
    # Se for admin, retorna todos os eventos
    if user.role == "admin":
        query_event = db.query(Event).all()
    else:
        # Se não, retorna apenas eventos do usuário
        query_event = db.query(Event).filter(Event.user_id == user.id).all()
    # Se não encontrar eventos, retorna erro 404
    if not query_event:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado")
    # Retorna lista de eventos
    return query_event

def get_event_by_id(db: Session, event_id: int, user: User):
    # Se for admin, pode buscar qualquer evento por id
    if user.role == "admin":
        event = db.query(Event).filter(Event.id == event_id).first()
    else:
        # Se não, só pode buscar eventos do próprio usuário
        event = db.query(Event).filter(Event.id == event_id, Event.user_id == user.id).first()
    # Se não encontrar, retorna erro 404
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    # Retorna o evento encontrado
    return event

def delete_event(db: Session, user: User, event: Event):
    # Se for admin, pode deletar permanentemente
    if user.role == "admin":
        db.delete(event)
        db.commit()
        return event  # Retorne o evento deletado (pode ser o objeto antes do delete)
    # Se não for admin, só pode cancelar se for o dono
    if event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    # Soft delete: altera status para "Cancelado"
    event.status = "Cancelado"
    db.commit()
    db.refresh(event)
    return event