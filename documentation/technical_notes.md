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
    event: EventCreate,                              # body validado pelo Pydantic
    db: Session = Depends(get_db),                   # sessão do banco
    current_user: User = Depends(get_current_user)   # usuário autenticado
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

---

## `services/` — Lógica de Negócio

A pasta `services` serve para separar a **receita** (lógica) da **entrega** (rota). Em vez de deixar a manipulação do banco espalhada nos routers, criamos funções dedicadas nos arquivos de serviço.

**Desacoplamento:** a rota cuida apenas de receber a requisição e devolver a resposta. O serviço cuida das regras de negócio como validar senha, verificar permissões e aplicar regras de negócio.

**Reuso:** se você precisar trocar a senha de um usuário via script de terminal ou tarefa agendada, você chama a mesma função do serviço sem precisar de uma requisição HTTP.

**Testabilidade:** é muito mais fácil criar testes unitários para uma função pura de serviço do que para uma rota que depende de todo o contexto do FastAPI.

```python
# router — só recebe e devolve
@router.post('/me/change-password')
def change_password(data: PasswordChange, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user_password(db, current_user, data)

# service — faz o trabalho pesado
def update_user_password(db: Session, user: User, data: PasswordChange) -> User:
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    db.refresh(user)
    return user
```

---

## `UserUpdate` e `exclude_unset` — Atualização Parcial com Pydantic

Ao criar um schema para atualização, os campos são `Optional` porque o usuário pode querer alterar só o email sem mexer no nome. O segredo está no `.model_dump(exclude_unset=True)`.

**`exclude_unset=True`:** garante que o Pydantic ignore campos que o usuário não enviou. Se só o email foi enviado, o `name` não é sobrescrito como `None` no banco.

**Atualização dinâmica com `setattr`:** em vez de escrever uma linha para cada campo, usamos um loop que aplica as mudanças automaticamente independente de quantos campos o schema tiver.

```python
update_data = user_data.model_dump(exclude_unset=True)

for key, value in update_data.items():
    setattr(current_user, key, value)

db.commit()
db.refresh(current_user)
```

---

## Regras de Argumentos: Python puro vs FastAPI

Existe uma diferença importante entre funções de serviço (Python puro) e rotas do FastAPI.

### Python puro — regra rígida
Argumentos obrigatórios devem vir **antes** de argumentos com valor padrão. Violar isso gera `SyntaxError`.

```python
# ❌ Errado
def func(opcional=1, obrigatorio: str): ...

# ✅ Certo
def func(obrigatorio: str, opcional=1): ...
```

A anotação de tipo com `:` não é valor padrão, é só uma dica de tipo. Valor padrão é só quando tem `=`.

### FastAPI routers — aparentemente flexível
Nas rotas o FastAPI parece ignorar a ordem porque o `Depends()` tecnicamente atribui um valor padrão ao argumento. Por isso os schemas (obrigatórios, sem `=`) geralmente vêm primeiro e as dependências (`= Depends(...)`) vêm por último.

```python
# FastAPI entende isso sem problema
def create_event(
    event: EventCreate,                            # obrigatório, sem =
    db: Session = Depends(get_db),                 # tem = portanto opcional
    current_user: User = Depends(get_current_user) # tem = portanto opcional
):
```

---

## Segurança: Troca de Senha

A troca de senha nunca deve estar no mesmo endpoint que edita nome ou email. Ela exige um fluxo próprio por dois motivos:

**Validação da senha atual:** antes de salvar a nova senha, o sistema precisa confirmar com `verify_password` que quem está trocando é o dono da conta.

**Endpoint isolado:** usar `POST /users/me/change-password` evita que uma edição acidental de perfil altere ou apague a senha sem querer.

```python
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
```

---

## OAuth2 e o formato `form-data`

Quando você usa `OAuth2PasswordBearer` no FastAPI, a rota de login espera os dados no formato `application/x-www-form-urlencoded`, não JSON. Isso segue a especificação OAuth2.

```python
# No backend, use OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.username).first()
    ...
```

No frontend, ao invés de `JSON.stringify`, você precisa usar `URLSearchParams`:

```javascript
const formData = new URLSearchParams();
formData.append('username', email);
formData.append('password', senha);

fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData
});
```

---

## Tratamento de Erros de Integridade no Banco

Quando o usuário tenta salvar um email que já existe, o `db.commit()` lança um `IntegrityError`. Sem tratar isso o sistema retorna um erro 500 genérico e confuso.

```python
from sqlalchemy.exc import IntegrityError

try:
    db.commit()
    db.refresh(current_user)
except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
```

O `db.rollback()` é obrigatório aqui. Se você não desfizer a transação com erro, a sessão fica em estado inválido e as próximas operações podem falhar.