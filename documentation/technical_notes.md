# 📝 Notas Técnicas — UaiFestas
> Escritas durante o desenvolvimento. Conceitos explicados com minhas próprias palavras.

---

## `config.py`

O `config.py` é uma forma de acessar as variáveis do `.env` sem que nenhum arquivo do projeto acesse o `.env` diretamente. Em vez de fazer `os.getenv("SECRET_KEY")` espalhado pelo código, você centraliza tudo em uma classe `Settings` e importa o objeto `settings` onde precisar.

O Pydantic valida os tipos automaticamente. Se você declarou `ACCESS_TOKEN_EXPIRE_MINUTES: int` e o valor no `.env` for a string `"30"`, ele converte para inteiro sozinho. Se uma variável obrigatória estiver faltando no `.env`, ele lança erro na hora que a aplicação sobe, antes de qualquer rota ser chamada.

```python
from config import settings

engine = create_engine(settings.DATABASE_URL)  # acessa sem saber o valor real
```

**Por que isso importa:** nenhum arquivo do projeto conhece os valores reais de senha, chave secreta ou URL do banco. Tudo fica no `.env` que está no `.gitignore` e nunca vai para o GitHub.

---

## `database.py`

Responsável por criar a conexão com o PostgreSQL e fornecer as ferramentas que o resto do projeto usa para falar com o banco.

### Engine
O `engine` é o objeto de conexão real com o banco de dados. Ele usa a `DATABASE_URL` do `settings` para saber onde o PostgreSQL está rodando, qual usuário usar, qual senha e qual banco acessar. Pensa nele como o "cabo" que liga sua aplicação ao banco. Sem ele nada chega no PostgreSQL.

```python
engine = create_engine(settings.DATABASE_URL)
# DATABASE_URL = postgresql://postgres:senha@localhost:5432/uaifestas
#                              usuario  senha    host      porta  banco
```

### SessionLocal
É uma fábrica de sessões, não uma sessão em si. Cada vez que uma rota precisa falar com o banco, essa fábrica cria uma sessão nova, isolada para aquela requisição.

- `autocommit=False` — nenhuma alteração é salva no banco automaticamente. Você precisa chamar `db.commit()` explicitamente. Se algo der errado você pode chamar `db.rollback()` e desfazer tudo.
- `autoflush=False` — o SQLAlchemy não envia queries para o banco automaticamente antes de cada consulta. Você controla quando isso acontece, evitando comportamentos inesperados.
- `bind=engine` — fala para a sessão qual engine usar, ou seja, qual banco, login e senha.

### Base
É a classe que todos os models herdam. Quando você escreve `class User(Base)`, o SQLAlchemy entende que essa classe representa uma tabela no banco e sabe como transformar os atributos da classe em colunas SQL.

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

Sem herdar o `Base`, o SQLAlchemy não reconhece a classe como uma tabela.

---

## `dependencies.py`

Responsável por abrir uma sessão do banco para cada requisição de forma isolada e garantir que ela sempre seja fechada ao final, com ou sem erro.

```python
def get_db():
    db = SessionLocal()   # cria a sessão
    try:
        yield db          # entrega para a rota usar
    finally:
        db.close()        # fecha sempre, mesmo se der erro
```

O `yield` é o que faz a mágica aqui. Diferente do `return` que encerra a função ao entregar o valor, o `yield` pausa a função, entrega a sessão para a rota, e só continua executando o `finally` depois que a rota terminar. Isso garante que a sessão **sempre** vai ser fechada.

Cada requisição tem sua própria sessão. Se duas pessoas acessam a API ao mesmo tempo, cada uma recebe uma sessão separada e independente.

---

## `Depends` — Injeção de Dependências no FastAPI

O `Depends` é o mecanismo do FastAPI para resolver dependências antes de executar uma rota. Quando você declara `db: Session = Depends(get_db)`, o FastAPI chama o `get_db` automaticamente antes de entrar na função da rota.

Se a dependência falhar, a rota não é executada.

### Fluxo completo de uma rota autenticada

```python
def create_event(
    event: EventCreate,                              # 3
    db: Session = Depends(get_db),                   # 1
    current_user: User = Depends(get_current_user)   # 2
):
```

O FastAPI resolve nessa ordem:

**1. `get_db`** — abre a sessão com o banco. Se o banco estiver fora do ar, para aqui e retorna erro 500.

**2. `get_current_user`** — pega o header `Authorization` da requisição, extrai o JWT, valida a assinatura com a `SECRET_KEY`, verifica se não está expirado, busca o usuário no banco. Se o token for inválido ou expirado, para aqui e retorna 401 automaticamente.

**3. Validação do body** — o FastAPI pega o JSON do body da requisição e valida contra o schema `EventCreate` usando Pydantic. Se estiver faltando campo obrigatório ou com tipo errado, retorna 422 automaticamente.

**Só depois de tudo isso resolvido** o código dentro da função começa a executar.

---

## Resumo do fluxo geral

```
Requisição HTTP
      ↓
FastAPI recebe
      ↓
Resolve Depends (get_db → get_current_user → valida body)
      ↓
Executa a função da rota
      ↓
Retorna resposta
      ↓
finally: db.close()
```