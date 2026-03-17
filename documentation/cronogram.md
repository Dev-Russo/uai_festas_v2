# 🎉 UaiFestas — Cronograma Project-Based Learning
## Roadmap Revisado: 12 Semanas | AI Engineer via Produto Real

---

## 📌 Por que mudamos o cronograma?

O cronograma anterior foi construído no modelo tradicional de **estudo → projeto**, onde você aprenderia os conceitos em semanas separadas e só depois aplicaria em projetos reais. Ele funcionaria bem em um cenário de dedicação exclusiva, mas apresentava três problemas práticos para a sua situação:

**1. Carga incompatível com estágio.** 4 horas de estudo estruturado por dia, conciliando estágio, é uma receita para burnout nas primeiras semanas. A consistência ao longo de 3 meses vale muito mais do que intensidade insustentável.

**2. Aprendizado no vácuo desmotiva.** Estudar LangChain sem um problema real para resolver é infinitamente mais árido do que aprender LangChain porque você precisa dele para fazer o assistente do UaiFestas funcionar. A motivação intrínseca acelera o aprendizado.

**3. Portfólio fraco.** Ao final de 3 meses com o modelo anterior, você teria vários mini-projetos acadêmicos. Com o novo modelo, você tem um produto real, com usuários reais, com decisões técnicas reais para contar em entrevista. Isso fecha vaga.

**A nova abordagem é Project-Based Learning:** o UaiFestas é o fio condutor de todo o aprendizado. Cada tecnologia do roadmap é introduzida quando o produto precisa dela, não antes. O DSA continua com 1 LeetCode por dia, mas integrado à rotina sem peso adicional.

---

## 🗺️ Visão Geral das 12 Semanas

| Semana | Entrega do Produto | Stack Introduzida |
|--------|-------------------|-------------------|
| 1 | Backend base: Auth + Eventos + Produtos | FastAPI, Pydantic, SQLAlchemy, Alembic |
| 2 | Vendas + Dashboard básico + Testes | Pytest, PostgreSQL, relações SQLAlchemy |
| 3 | Importação de CSV + Normalização | Pandas, tratamento de dados, novos endpoints |
| 4 | Dashboard inteligente com métricas reais | Pandas avançado, Numpy, análise de dados |
| 5 | Assistente LLM básico (perguntas sobre o evento) | OpenAI API, prompting, structured output |
| 6 | Assistente com memória e contexto | LangChain, LCEL, ConversationMemory |
| 7 | Base de conhecimento de marketing | ChromaDB, FAISS, embeddings |
| 8 | RAG completo aplicado ao produto | RAG end-to-end, LangChain retrievers |
| 9 | Alertas proativos e agente autônomo | LangGraph, agentes, tool calling |
| 10 | Observabilidade e qualidade da IA | LangSmith, RAGAS, logs estruturados |
| 11 | Deploy em produção + CI/CD | Docker, GitHub Actions, Azure/AWS |
| 12 | MLOps + Polimento + Usuários reais | MLOps básico, LLMOps, portfólio |

---

## 🟢 SEMANA 1 — Backend Base: Autenticação + Eventos + Produtos

### 🎯 Objetivo do Produto
Ter o esqueleto completo do sistema funcionando: um produtor consegue se cadastrar, fazer login e criar um evento com seus produtos (lotes de ingresso).

### 📦 Funcionalidades a Entregar

#### Autenticação
- `POST /auth/register` — cadastro de usuário com nome, email e senha
- `POST /auth/login` — retorna JWT token
- Middleware de autenticação protegendo rotas privadas
- Hash de senha com `bcrypt`
- Expiração de token configurável

#### Usuários
- `GET /users/me` — retorna dados do usuário autenticado
- `PUT /users/me` — atualiza nome e senha
- Roles: `admin` e `producer` (produtor de festa)

#### Eventos
- `POST /events` — cria evento (nome, descrição, data, local)
- `GET /events` — lista eventos do usuário autenticado
- `GET /events/{id}` — detalhe do evento
- `PUT /events/{id}` — atualiza evento
- `DELETE /events/{id}` — cancela evento (soft delete, muda status)
- Status do evento: `draft`, `active`, `completed`, `cancelled`

#### Produtos (Lotes)
- `POST /events/{id}/products` — cria lote (nome, preço, quantidade, data início, data fim)
- `GET /events/{id}/products` — lista lotes do evento
- `PUT /events/{id}/products/{product_id}` — atualiza lote
- `DELETE /events/{id}/products/{product_id}` — remove lote

#### Banco de Dados
- PostgreSQL com SQLAlchemy ORM
- Migrations com Alembic
- Tabelas: `users`, `events`, `products`
- Relacionamento: um usuário tem muitos eventos, um evento tem muitos produtos

### ✅ Critérios Mínimos de Aceitação
- [ ] É possível criar um usuário, fazer login e receber um JWT válido
- [ ] Rotas protegidas retornam 401 sem token e funcionam com token válido
- [ ] CRUD completo de eventos funcionando via Swagger
- [ ] CRUD completo de produtos vinculados a evento funcionando
- [ ] Migrations rodando com `alembic upgrade head` sem erros
- [ ] Nenhuma senha armazenada em texto puro no banco
- [ ] Usuário só acessa seus próprios eventos (não consegue ver evento de outro usuário)

### 📚 Conceitos que Você Vai Aprender Fazendo
- Estrutura de projeto FastAPI com routers, schemas, models e utils separados
- Como funcionam JWTs na prática (geração, validação, expiração)
- SQLAlchemy: models, relacionamentos, sessões
- Alembic: criando e rodando migrations
- Pydantic: validação de entrada e saída com BaseModel

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| FastAPI do Zero — Dunossauro (fastapidozero.dunossauro.com) | Referência principal da semana |
| Documentação oficial FastAPI — Security | Ao implementar JWT |
| Documentação SQLAlchemy ORM | Ao criar os models |
| Alembic Tutorial oficial | Ao configurar migrations |

### 🏋️ LeetCode da Semana (Easy)
- Seg: Two Sum (#1)
- Ter: Valid Parentheses (#20)
- Qua: Palindrome Number (#9)
- Qui: Contains Duplicate (#217)
- Sex: Best Time to Buy and Sell Stock (#121)

---

## 🟢 SEMANA 2 — Vendas + Dashboard Básico + Testes

### 🎯 Objetivo do Produto
O produtor consegue registrar vendas manualmente e visualizar um painel básico com números reais do seu evento. O sistema tem cobertura de testes.

### 📦 Funcionalidades a Entregar

#### Vendas
- `POST /events/{id}/sales` — registra venda (produto, comprador, método de pagamento, preço)
- `GET /events/{id}/sales` — lista todas as vendas do evento
- `GET /events/{id}/sales/{sale_id}` — detalhe da venda
- `PATCH /events/{id}/sales/{sale_id}/cancel` — cancela uma venda
- `PATCH /events/{id}/sales/{sale_id}/checkin` — faz check-in do ingresso
- Status da venda: `paid`, `cancelled`, `checked_in`
- Geração de código único por venda (UUID)
- Tabela `sales` com: produto, comprador (nome + email), método pagamento, preço, status, data

#### Dashboard Básico
- `GET /events/{id}/dashboard` — retorna:
  - Total de vendas pagas
  - Total de vendas canceladas
  - Receita total
  - Ticket médio
  - Vendas por produto (ranking)
  - Vendas por dia (últimos 30 dias)
  - Taxa de cancelamento

#### Testes com Pytest
- Testes de autenticação (registro, login, token inválido)
- Testes de CRUD de eventos
- Testes de CRUD de vendas
- Testes do dashboard (valores calculados corretamente)
- Uso de banco de dados em memória (SQLite) para testes
- Fixtures para criar usuário e evento padrão nos testes

### ✅ Critérios Mínimos de Aceitação
- [ ] É possível registrar uma venda e ela aparece no dashboard imediatamente
- [ ] Cancelamento de venda atualiza os totais do dashboard corretamente
- [ ] Dashboard retorna os 7 campos listados sem nenhum zerado incorretamente
- [ ] Pelo menos 15 testes passando com `pytest`
- [ ] Cobertura de testes acima de 60% nas rotas principais
- [ ] Check-in registra o horário e muda o status da venda
- [ ] Código único de cada venda é realmente único (UUID)

### 📚 Conceitos que Você Vai Aprender Fazendo
- Agregações com SQLAlchemy (`func.sum`, `func.count`, `group_by`)
- Pytest: fixtures, TestClient do FastAPI, banco de teste isolado
- Modelagem de status com enums
- Queries com filtros de data e período

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| FastAPI do Zero — capítulo de testes | Ao configurar Pytest |
| SQLAlchemy — Core Aggregations docs | Ao implementar dashboard |
| ArjanCodes — Pytest playlist | Para boas práticas de teste |

### 🏋️ LeetCode da Semana (Easy)
- Seg: Maximum Subarray (#53)
- Ter: Climbing Stairs (#70)
- Qua: Merge Sorted Array (#88)
- Qui: Valid Anagram (#242)
- Sex: Reverse Linked List (#206)

---

## 🟡 SEMANA 3 — Importação de CSV + Normalização de Dados

### 🎯 Objetivo do Produto
O produtor não precisa mais registrar vendas manualmente. Ele exporta o relatório da Sympla ou Ingresse, faz upload do CSV e o sistema importa tudo automaticamente, normalizando os dados independente da plataforma de origem.

### 📦 Funcionalidades a Entregar

#### Upload e Importação de CSV
- `POST /events/{id}/import` — recebe arquivo CSV via multipart/form-data
- Detecção automática da plataforma de origem (Sympla, Ingresse, formato genérico)
- Normalização dos campos para o formato interno do sistema
- Retorno de relatório de importação: total importado, duplicatas ignoradas, erros encontrados
- Importações duplicadas não geram vendas duplicadas (verificação por código único ou combinação comprador + produto + data)

#### Mapeamento de Plataformas
- Sympla: mapear colunas do CSV exportado para os campos internos
- Ingresse: mapear colunas do CSV exportado para os campos internos
- Formato genérico: template CSV disponível para download com as colunas esperadas
- `GET /events/{id}/import/template` — retorna CSV template para preenchimento manual

#### Histórico de Importações
- `GET /events/{id}/imports` — lista todas as importações realizadas
- Cada importação registra: data, plataforma, total de linhas, importadas, ignoradas, erros

#### Validação de Dados
- Campos obrigatórios por linha do CSV
- Tratamento de datas em formatos diferentes (BR e ISO)
- Tratamento de valores monetários (R$ 50,00 → 50.0)
- Linhas com erro não bloqueiam o restante da importação
- Log de erros por linha para o produtor corrigir

### ✅ Critérios Mínimos de Aceitação
- [ ] Upload de CSV da Sympla importa as vendas corretamente no banco
- [ ] Upload do mesmo CSV duas vezes não duplica vendas
- [ ] Relatório de importação informa exatamente quantas linhas foram importadas, ignoradas e com erro
- [ ] Valores monetários com vírgula (padrão BR) são convertidos corretamente
- [ ] Template CSV para download funciona e ao reimportar popula os dados certos
- [ ] Importação de 500 linhas leva menos de 10 segundos
- [ ] Testes cobrindo os cenários de duplicata, erro e sucesso

### 📚 Conceitos que Você Vai Aprender Fazendo
- Pandas: leitura de CSV, normalização de colunas, tratamento de nulos
- Upload de arquivos com FastAPI (`UploadFile`)
- Processamento em lote com SQLAlchemy (bulk insert)
- Tratamento de erros linha a linha sem abortar operação

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| FastAPI docs — File Upload | Ao implementar o endpoint de upload |
| Pandas docs — read_csv | Ao processar o arquivo |
| Corey Schafer — Pandas Tutorial YouTube | Para se familiarizar com Pandas |

### 🏋️ LeetCode da Semana (Easy/Medium)
- Seg: Find All Duplicates in Array (#442)
- Ter: Group Anagrams (#49)
- Qua: Product of Array Except Self (#238)
- Qui: Longest Consecutive Sequence (#128)
- Sex: Top K Frequent Elements (#347)

---

## 🟡 SEMANA 4 — Dashboard Inteligente com Métricas Reais

### 🎯 Objetivo do Produto
O dashboard deixa de mostrar só totais e passa a mostrar inteligência de negócio real: velocidade de vendas, previsão de esgotamento de lote, horários de pico, comparação entre períodos e análise de performance por lote.

### 📦 Funcionalidades a Entregar

#### Métricas Avançadas de Vendas
- Velocidade de vendas: ingressos vendidos por hora nas últimas 24h, 7 dias e 30 dias
- Previsão de esgotamento: baseado na velocidade atual, em quantos dias o lote esgota
- Comparação entre lotes: qual lote está vendendo mais rápido proporcionalmente
- Heatmap de vendas por hora do dia e dia da semana
- Receita acumulada ao longo do tempo (curva de crescimento)

#### Análise de Lotes
- Para cada lote: % vendido, velocidade, dias até esgotar, receita gerada
- Alerta de lote com estoque crítico (menos de 10% disponível)
- Comparação de performance entre lotes do mesmo evento

#### Comparação de Períodos
- Comparar semana atual vs semana anterior
- Comparar com média de eventos anteriores do mesmo produtor
- Crescimento percentual de receita e volume

#### Endpoint de Resumo Executivo
- `GET /events/{id}/dashboard/summary` — retorna em linguagem estruturada (JSON) um resumo do evento: status atual, principais alertas, destaques positivos

### ✅ Critérios Mínimos de Aceitação
- [ ] Velocidade de vendas calculada corretamente para os 3 períodos
- [ ] Previsão de esgotamento aparece em dias inteiros com base na velocidade real
- [ ] Heatmap retorna dados organizados por hora (0-23) e dia da semana (0-6)
- [ ] Comparação de períodos mostra delta absoluto e percentual
- [ ] Summary endpoint retorna JSON estruturado com pelo menos: total vendido, receita, lote mais vendido, alerta de estoque crítico se houver
- [ ] Todos os cálculos têm testes unitários verificando os valores

### 📚 Conceitos que Você Vai Aprender Fazendo
- Pandas: groupby por hora e dia, rolling windows, resample
- Numpy: operações vetorizadas para cálculos de velocidade
- Estatística básica aplicada: médias móveis, projeções lineares simples
- Serialização de dados complexos com Pydantic

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| Statquest — Statistics Fundamentals YouTube | Para entender os cálculos estatísticos |
| Pandas docs — GroupBy e Resample | Para os agrupamentos por tempo |
| Sigmoidal YouTube — Análise de dados com Pandas | Exemplos práticos em PT-BR |

### 🏋️ LeetCode da Semana (Medium)
- Seg: 3Sum (#15)
- Ter: Container With Most Water (#11)
- Qua: Sliding Window Maximum (#239)
- Qui: Minimum Size Subarray Sum (#209)
- Sex: Longest Substring Without Repeating Characters (#3)

---

## 🟠 SEMANA 5 — Assistente LLM: Perguntas sobre o Evento

### 🎯 Objetivo do Produto
O produtor consegue conversar com o sistema em linguagem natural sobre os dados do seu evento. Digita "meu lote 2 está devagar, o que fazer?" e recebe uma resposta contextualizada com os dados reais de vendas.

### 📦 Funcionalidades a Entregar

#### Endpoint de Chat com o Evento
- `POST /events/{id}/chat` — recebe pergunta em texto livre, retorna resposta da IA
- O sistema injeta automaticamente os dados do evento no contexto (métricas do dashboard, lotes, velocidade de vendas)
- Resposta sempre referencia dados reais ("seu lote 1 vendeu 234 ingressos nas últimas 48h...")
- Structured output: além do texto, retorna `action_items` (lista de ações sugeridas) e `urgency` (low/medium/high)

#### Categorização de Intenção
- O sistema classifica a pergunta em categorias: `vendas`, `marketing`, `operacional`, `previsão`
- Cada categoria direciona o contexto injetado no prompt

#### Histórico de Perguntas
- `GET /events/{id}/chat/history` — lista as últimas 20 perguntas e respostas
- Armazenado no banco de dados vinculado ao evento

#### Configuração de API Key
- Produtor pode configurar sua própria OpenAI API Key nas configurações da conta
- Sistema usa chave do produtor se disponível, chave do sistema como fallback

### ✅ Critérios Mínimos de Aceitação
- [ ] Pergunta sobre vendas retorna resposta que menciona números reais do evento
- [ ] Structured output sempre retorna `action_items` como lista e `urgency` como enum válido
- [ ] Pergunta sobre lote específico ("como está o lote 2?") retorna dados daquele lote
- [ ] Histórico de chat funciona e persiste entre sessões
- [ ] Custo estimado em tokens é logado por requisição
- [ ] Resposta chega em menos de 10 segundos
- [ ] Testes mockando a OpenAI API (sem consumir créditos no teste)

### 📚 Conceitos que Você Vai Aprender Fazendo
- OpenAI API: `chat.completions.create`, messages array, system/user/assistant roles
- Structured output com JSON mode e validação Pydantic
- Prompt engineering: injeção de contexto dinâmico, few-shot para formato de resposta
- Como calcular e logar custo de tokens (`prompt_tokens`, `completion_tokens`)
- Mocking de APIs externas em testes com `pytest-mock`

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| OpenAI Cookbook — cookbook.openai.com | Referência principal da semana |
| Prompt Engineering Guide — promptingguide.ai/pt | Para estruturar os prompts |
| Andrej Karpathy — Intro to LLMs YouTube | Para entender o que está acontecendo por baixo |
| Sam Witteveen YouTube — OpenAI Function Calling | Para structured output |

### 🏋️ LeetCode da Semana (Medium)
- Seg: Search in Rotated Sorted Array (#33)
- Ter: Find Minimum in Rotated Sorted Array (#153)
- Qua: Binary Search (#704)
- Qui: Time Based Key-Value Store (#981)
- Sex: Koko Eating Bananas (#875)

---

## 🟠 SEMANA 6 — Assistente com Memória e Contexto (LangChain)

### 🎯 Objetivo do Produto
O assistente passa a lembrar da conversa anterior e responde com mais inteligência ao longo de um diálogo. O produtor pode fazer perguntas de acompanhamento sem repetir o contexto.

### 📦 Funcionalidades a Entregar

#### Refatoração com LangChain
- Substituir chamada direta da OpenAI por LangChain LCEL chains
- `ChatPromptTemplate` com variáveis dinâmicas de contexto do evento
- `StrOutputParser` e `JsonOutputParser` para os diferentes tipos de resposta
- Chain de análise: recebe dados do evento → analisa → retorna insights estruturados

#### Memória de Conversa
- `ConversationBufferMemory` para manter histórico na sessão
- Após 10 mensagens, comprime o histórico com `ConversationSummaryMemory`
- Memória persistida no banco de dados por evento e por usuário

#### Chains Especializadas
- Chain de diagnóstico de vendas: analisa métricas e identifica problemas
- Chain de sugestão de ação: dado um problema, sugere ações específicas
- Chain de previsão: dado o ritmo atual, projeta cenários
- As chains são conectadas via LCEL pipe operator

#### Endpoint de Análise Automática
- `POST /events/{id}/analyze` — sem input do usuário, o sistema analisa o evento e retorna um relatório completo com diagnóstico, alertas e recomendações

### ✅ Critérios Mínimos de Aceitação
- [ ] Pergunta de acompanhamento ("e o lote 3?") funciona sem repetir contexto
- [ ] Memória é mantida por pelo menos 10 mensagens sem perder contexto relevante
- [ ] Chain de análise automática retorna diagnóstico com pelo menos 3 seções: situação atual, alertas e recomendações
- [ ] Código não tem mais chamadas diretas à OpenAI, tudo passa pelo LangChain
- [ ] Chains são testáveis de forma isolada
- [ ] Tempo de resposta com memória não aumenta mais de 2s em relação à semana anterior

### 📚 Conceitos que Você Vai Aprender Fazendo
- LangChain LCEL: pipe operator, RunnablePassthrough, RunnableParallel
- ChatPromptTemplate com input variables
- Memory: Buffer vs Summary, quando usar cada um
- Composição de chains em pipeline
- Por que abstrair sobre o modelo (trocar GPT por Claude sem mudar código)

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| LangChain docs — python.langchain.com | Referência principal |
| LangChain YouTube oficial | Tutoriais de LCEL e Memory |
| Sandeco YouTube — LangChain em PT-BR | Para exemplos em português |
| Greg Kamradt (DataIndependent) YouTube | LangChain na prática |

### 🏋️ LeetCode da Semana (Medium)
- Seg: Number of Islands (#200)
- Ter: Max Area of Island (#695)
- Qua: Clone Graph (#133)
- Qui: Rotting Oranges (#994)
- Sex: Walls and Gates (#286)

---

## 🟠 SEMANA 7 — Base de Conhecimento de Marketing de Eventos

### 🎯 Objetivo do Produto
O assistente passa a responder com base em conhecimento especializado de marketing para festas universitárias, não apenas com base nos dados do evento. As respostas ficam muito mais ricas e acionáveis.

### 📦 Funcionalidades a Entregar

#### Construção da Knowledge Base
- Curadoria de conteúdo: boas práticas de virada de lote, estratégias de divulgação no Instagram, timing de abertura de vendas, gatilhos de urgência, recuperação de vendas estagnadas
- Mínimo de 30 documentos na base (podem ser textos curtos e objetivos)
- Organização por categoria: `pricing`, `marketing`, `timing`, `recovery`, `checklist`
- Embeddings gerados com `text-embedding-3-small` da OpenAI

#### ChromaDB como Vector Store
- Instalação e configuração com persistência em disco
- Collection separada por categoria de conhecimento
- Metadados por documento: categoria, fonte, data de criação
- Busca por similaridade retornando top-5 documentos relevantes

#### FAISS como Alternativa
- Mesma base indexada em FAISS para comparação de performance
- Benchmark simples: tempo de busca ChromaDB vs FAISS para 100 queries

#### Endpoint de Busca Semântica
- `GET /knowledge/search?q=como+aumentar+vendas+lote` — busca na base de conhecimento
- Retorna documentos relevantes com score de similaridade
- Útil para debug e para o produtor entender de onde vem cada sugestão

### ✅ Critérios Mínimos de Aceitação
- [ ] Base de conhecimento tem pelo menos 30 documentos indexados no ChromaDB
- [ ] Busca semântica retorna resultados relevantes para queries sobre marketing de eventos
- [ ] Metadados de categoria funcionam como filtro na busca
- [ ] Dados do ChromaDB persistem após reiniciar o servidor
- [ ] Endpoint de busca retorna resultados em menos de 500ms
- [ ] Benchmark ChromaDB vs FAISS documentado em comentário no código

### 📚 Conceitos que Você Vai Aprender Fazendo
- O que são embeddings de verdade (representação numérica de semântica)
- ChromaDB: collections, add, query, metadados
- FAISS: IndexFlatL2, add, search
- Chunking de texto para indexação
- Similaridade de cosseno na prática

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| ChromaDB docs — docs.trychroma.com | Referência principal |
| James Briggs YouTube — Embeddings e Vector DBs | Para entender embeddings |
| Fireship YouTube — Vector Databases Explained | Visão geral rápida |
| Sandeco YouTube — Bancos vetoriais PT-BR | Para exemplos em português |

### 🏋️ LeetCode da Semana (Medium)
- Seg: Kth Largest Element in Array (#215)
- Ter: Sort Colors (#75)
- Qua: Meeting Rooms II (#253)
- Qui: Task Scheduler (#621)
- Sex: Find K Closest Elements (#658)

---

## 🔴 SEMANA 8 — RAG Completo Aplicado ao Produto

### 🎯 Objetivo do Produto
O assistente agora combina os dados reais do evento com o conhecimento especializado de marketing. Uma pergunta como "meu lote 2 está devagar" gera uma resposta que usa tanto os números do evento quanto as melhores práticas da base de conhecimento.

### 📦 Funcionalidades a Entregar

#### Pipeline RAG End-to-End
- Fase de Recuperação: pergunta do usuário → embedding → busca no ChromaDB → top-5 documentos relevantes
- Fase de Geração: contexto do evento + documentos recuperados + pergunta → LLM → resposta
- Citação das fontes: resposta indica quais documentos da base foram usados
- Fallback: se nenhum documento relevante for encontrado, responde só com dados do evento

#### RAG Avançado
- Query expansion: antes de buscar, o LLM reformula a pergunta para melhorar a recuperação
- Contextual compression: filtra partes irrelevantes dos documentos recuperados
- Re-ranking: após recuperar os 10 primeiros, re-ranqueia para retornar os 5 mais relevantes

#### Integração Completa com o Chat
- Substituir o chat da semana 6 pelo novo sistema RAG
- Cada resposta agora tem: texto, action_items, urgency, sources (lista de documentos usados)
- `GET /events/{id}/chat/{message_id}/sources` — retorna os documentos que embasaram uma resposta

### ✅ Critérios Mínimos de Aceitação
- [ ] Pergunta sobre estratégia de marketing retorna resposta que cita pelo menos 1 documento da base
- [ ] Campo `sources` na resposta lista os documentos usados com título e categoria
- [ ] Query expansion gera pelo menos 2 versões da pergunta antes de buscar
- [ ] Resposta com RAG é visivelmente mais rica em conteúdo do que sem RAG
- [ ] Fallback funciona: perguntas fora do domínio (ex: "qual a capital do Brasil") retornam resposta educada dizendo que está fora do escopo
- [ ] Testes de integração cobrindo o pipeline completo com mocks

### 📚 Conceitos que Você Vai Aprender Fazendo
- Pipeline RAG do zero ao deploy
- Query expansion e por que melhora a recuperação
- Contextual compression com LangChain
- Como avaliar se o RAG está funcionando bem (inspeção manual)
- Quando o RAG ajuda e quando atrapalha

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| LangChain YouTube — RAG from Scratch playlist | Referência principal da semana |
| James Briggs YouTube — Advanced RAG | Para técnicas avançadas |
| Sandeco YouTube — RAG em PT-BR | Para exemplos em português |
| LlamaIndex Blog — blog.llamaindex.ai | Para técnicas de Advanced RAG |

### 🏋️ LeetCode da Semana (Medium)
- Seg: Word Search (#79)
- Ter: Subsets (#78)
- Qua: Combination Sum (#39)
- Qui: Permutations (#46)
- Sex: Letter Combinations of a Phone Number (#17)

---

## 🔴 SEMANA 9 — Alertas Proativos e Agente Autônomo

### 🎯 Objetivo do Produto
O sistema para de esperar o produtor perguntar e começa a agir por conta própria. Detecta queda de vendas, lote prestes a esgotar ou oportunidade de ação e envia alertas com sugestões concretas.

### 📦 Funcionalidades a Entregar

#### Sistema de Alertas
- Job agendado que roda a cada hora verificando todos os eventos ativos
- Tipos de alerta: `stock_critical` (< 10% do lote), `sales_slowdown` (velocidade caiu > 30%), `no_sales_24h`, `event_approaching` (evento em menos de 7 dias com lotes disponíveis)
- `GET /events/{id}/alerts` — lista alertas ativos do evento
- `PATCH /events/{id}/alerts/{alert_id}/dismiss` — produtor descarta o alerta

#### Agente com LangGraph
- Grafo de estados para o fluxo de análise proativa
- Node de coleta: busca dados do evento
- Node de análise: identifica problemas e oportunidades
- Node de conhecimento: busca no RAG estratégias relevantes para o problema encontrado
- Node de geração: cria mensagem de alerta personalizada com ação sugerida
- Conditional edge: decide se o alerta é urgente (notificação imediata) ou informativo (agrupa no resumo diário)

#### Tools do Agente
- Tool `get_event_metrics` — busca métricas atuais do evento
- Tool `search_knowledge_base` — busca na base de conhecimento RAG
- Tool `calculate_projection` — calcula projeção de vendas

#### Resumo Diário por Email
- `POST /events/{id}/digest` — envia email com resumo do dia: vendas, alertas, recomendações
- Template de email em HTML com os dados do evento

### ✅ Critérios Mínimos de Aceitação
- [ ] Job de alertas roda a cada hora sem travar o servidor
- [ ] Alerta de estoque crítico é gerado quando lote chega em 10% ou menos
- [ ] Alerta de queda de vendas detecta corretamente redução > 30% na velocidade
- [ ] Agente LangGraph executa o fluxo completo em menos de 30 segundos
- [ ] Tools do agente são chamadas corretamente e retornam dados reais
- [ ] Email de resumo diário é enviado com dados corretos do evento
- [ ] Alertas podem ser descartados pelo produtor

### 📚 Conceitos que Você Vai Aprender Fazendo
- LangGraph: StateGraph, nodes, edges, conditional edges
- Background jobs com FastAPI (APScheduler ou Celery básico)
- Tool calling: definindo tools como funções Python decoradas
- Orquestração de agente com múltiplos passos
- Envio de email com Python (smtplib ou SendGrid)

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| LangGraph docs — langchain-ai.github.io/langgraph | Referência principal |
| LangChain YouTube — LangGraph tutorials | Para tutoriais práticos |
| APScheduler docs | Para jobs agendados |
| AI Jason YouTube | Agentes na prática |

### 🏋️ LeetCode da Semana (Medium/Hard)
- Seg: LRU Cache (#146)
- Ter: Min Stack (#155)
- Qua: Daily Temperatures (#739)
- Qui: Decode String (#394)
- Sex: Course Schedule (#207)

---

## 🔴 SEMANA 10 — Observabilidade e Qualidade da IA

### 🎯 Objetivo do Produto
O sistema passa a ser monitorado de verdade. Você consegue saber se a IA está respondendo bem, quanto está custando, onde está falhando e como melhorar.

### 📦 Funcionalidades a Entregar

#### Logging Estruturado
- Substituir todos os `print()` por logs estruturados com `loguru`
- Campos obrigatórios em todo log: `timestamp`, `event_id`, `user_id`, `request_id`, `level`
- Log de cada requisição à IA: modelo usado, tokens consumidos, latência, custo estimado
- Log de cada busca no RAG: query, documentos recuperados, scores de similaridade

#### LangSmith Integration
- Configuração do LangSmith para tracing automático
- Cada chain e agente rastreado com inputs, outputs e latência
- Tags por tipo de operação: `chat`, `analyze`, `alert`, `rag`
- Dashboard no LangSmith mostrando volume de requisições e latência média

#### Avaliação de Qualidade com RAGAS
- Dataset de avaliação: 20 pares de pergunta/resposta esperada criados manualmente
- Métricas calculadas: `faithfulness`, `answer_relevancy`, `context_precision`
- `GET /admin/rag-evaluation` — roda avaliação e retorna relatório de qualidade
- Score mínimo de qualidade definido como threshold

#### Dashboard de Custos
- `GET /admin/costs` — retorna custo total por evento, por usuário e por período
- Alerta quando custo de um evento ultrapassa threshold configurável
- Breakdown: custo de embeddings vs custo de geração

### ✅ Critérios Mínimos de Aceitação
- [ ] Todos os logs têm os campos estruturados obrigatórios
- [ ] LangSmith mostra traces de pelo menos 10 interações distintas
- [ ] RAGAS evaluation retorna os 3 scores para o dataset de 20 questões
- [ ] Score de faithfulness acima de 0.7 no dataset de avaliação
- [ ] Custo por requisição é logado com precisão de 4 casas decimais
- [ ] Dashboard de custos funcional e com dados reais

### 📚 Conceitos que Você Vai Aprender Fazendo
- Logging estruturado vs print: por que importa em produção
- Observabilidade: logs, métricas e traces (os 3 pilares)
- LangSmith: como rastrear LLMs em produção
- RAGAS: como avaliar RAG de forma quantitativa
- Custo de LLMs: como calcular e controlar

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| LangSmith docs — docs.smith.langchain.com | Configuração e uso |
| RAGAS docs — docs.ragas.io | Avaliação do RAG |
| ArjanCodes YouTube — Logging in Python | Logging estruturado |
| Full Stack Deep Learning YouTube — LLMOps | Contexto de observabilidade |

### 🏋️ LeetCode da Semana (Medium/Hard)
- Seg: Median of Two Sorted Arrays (#4)
- Ter: Trapping Rain Water (#42)
- Qua: Word Ladder (#127)
- Qui: Pacific Atlantic Water Flow (#417)
- Sex: Serialize and Deserialize Binary Tree (#297)

---

## 🔵 SEMANA 11 — Deploy em Produção + CI/CD

### 🎯 Objetivo do Produto
O UaiFestas sai do localhost e vai para uma URL pública real. Qualquer push na branch main dispara testes automáticos e deploy. Produtores reais podem começar a usar.

### 📦 Funcionalidades a Entregar

#### Docker
- `Dockerfile` para a aplicação FastAPI
- `docker-compose.yml` com: app, PostgreSQL e ChromaDB
- `.dockerignore` configurado
- Variáveis de ambiente via `.env` (nunca hardcoded)
- Health check endpoint: `GET /health`

#### GitHub Actions — CI/CD
- Pipeline de CI: roda em todo push e PR
  - Lint com `ruff`
  - Formatação com `black`
  - Testes com `pytest`
  - Build da imagem Docker
- Pipeline de CD: roda só na branch `main` após CI passar
  - Push da imagem para registry (Docker Hub ou GitHub Container Registry)
  - Deploy automático na cloud

#### Deploy na Cloud
- Escolha: Azure App Service (recomendado para aprender Azure AI Engineer) ou Railway (mais simples)
- PostgreSQL gerenciado na cloud (Azure Database for PostgreSQL ou Supabase)
- ChromaDB rodando em volume persistente
- Domínio configurado (pode ser subdomínio gratuito)
- HTTPS ativo

#### Configuração de Produção
- Variáveis de ambiente separadas por ambiente (dev, prod)
- Rate limiting nos endpoints de IA (evitar custo excessivo)
- CORS configurado corretamente para produção

### ✅ Critérios Mínimos de Aceitação
- [ ] `docker-compose up` sobe todo o ambiente local em um comando
- [ ] Push na branch `main` dispara o pipeline completo automaticamente
- [ ] Pipeline falha se algum teste falhar (não faz deploy com teste quebrado)
- [ ] Aplicação acessível via URL pública com HTTPS
- [ ] Nenhuma chave de API ou senha no código ou no repositório
- [ ] Health check retorna 200 em produção
- [ ] Logs de produção acessíveis remotamente

### 📚 Conceitos que Você Vai Aprender Fazendo
- Docker: containerização, camadas, build eficiente
- docker-compose: orquestração de múltiplos serviços
- GitHub Actions: workflows, triggers, secrets
- Deploy em cloud: conceitos de PaaS, variáveis de ambiente, volumes
- Segurança básica: secrets, HTTPS, rate limiting

### 🎥 Recursos de Apoio
| Recurso | Quando usar |
|---------|-------------|
| Fabio Akita YouTube — Docker do Zero | Para entender Docker de verdade |
| TechWorld with Nana YouTube — Docker Crash Course | Referência prática |
| GitHub Actions docs | Para configurar os workflows |
| Canal da Cloud YouTube — Azure PT-BR | Para deploy no Azure |
| Microsoft Learn — Azure Fundamentals (grátis) | Para certificação futura |

### 🏋️ LeetCode da Semana (Medium/Hard)
- Seg: Binary Tree Level Order Traversal (#102)
- Ter: Validate Binary Search Tree (#98)
- Qua: Lowest Common Ancestor (#236)
- Qui: Graph Valid Tree (#261)
- Sex: Word Search II (#212)

---

## 🏆 SEMANA 12 — MLOps, Polimento e Usuários Reais

### 🎯 Objetivo do Produto
O produto está em produção, monitorado, com MLOps básico implementado e com os primeiros usuários reais. O portfólio está documentado e você está pronto para entrevistas.

### 📦 Funcionalidades a Entregar

#### MLOps / LLMOps Básico
- Versionamento de prompts: cada prompt tem versão e é armazenado no banco, não hardcoded
- `GET /admin/prompts` — lista versões ativas dos prompts
- `PUT /admin/prompts/{name}` — atualiza prompt sem fazer redeploy
- A/B testing simples: 50% das requisições usam prompt A, 50% usam prompt B, métricas comparadas
- Rollback de prompt: se nova versão piora o score RAGAS, reverte automaticamente

#### Gestão de Usuários Reais
- Onboarding flow: email de boas-vindas com tutorial de como importar o primeiro CSV
- Limite de uso por plano (free: 1 evento ativo, 3 perguntas/dia para a IA)
- `GET /admin/users` — painel administrativo com lista de usuários e uso

#### Polimento Final
- README completo no GitHub com: problema, solução, arquitetura, tecnologias, como rodar localmente, como contribuir
- Diagrama de arquitetura (pode ser feito no draw.io)
- Documentação da API no Swagger completa e organizada
- Página de landing simples (pode ser uma página HTML estática) explicando o produto

#### Preparação para Entrevista
- Document de decisões técnicas: por que escolheu ChromaDB em vez de Pinecone, por que LangGraph para os alertas, etc.
- 5 perguntas técnicas que você consegue responder sobre o próprio projeto
- Demo script: roteiro de 5 minutos para apresentar o produto ao vivo

### ✅ Critérios Mínimos de Aceitação
- [ ] Pelo menos 1 usuário real usando o sistema (além de você)
- [ ] Versionamento de prompts funcionando (consegue mudar prompt sem redeploy)
- [ ] A/B test de prompt com métricas sendo coletadas
- [ ] README está completo e alguém consegue rodar o projeto localmente seguindo as instruções
- [ ] Diagrama de arquitetura publicado no README
- [ ] Consegue fazer uma demo ao vivo de 5 minutos sem travar
- [ ] Post no LinkedIn redigido e publicado com link para o GitHub e URL do produto

### 🏋️ LeetCode da Semana (revisão geral)
- Revisite os 5 problemas que você errou e não resolveu durante as semanas anteriores
- 1 mock interview completo no LeetCode (modo cronometrado, 45 minutos, 2 problemas medium)

---

## 📊 Stack Completa Aplicada ao Final das 12 Semanas

| Categoria | Tecnologia | Semana de Introdução |
|-----------|-----------|---------------------|
| Backend | FastAPI, Pydantic, SQLAlchemy, Alembic | 1 |
| Banco de Dados | PostgreSQL | 1 |
| Auth | JWT, bcrypt | 1 |
| Testes | Pytest, pytest-mock | 2 |
| Dados | Pandas, Numpy | 3-4 |
| LLMs | OpenAI API | 5 |
| Orquestração LLM | LangChain, LCEL | 6 |
| Vector Store | ChromaDB, FAISS | 7 |
| Arquitetura RAG | RAG, embeddings, retrievers | 8 |
| Agentes | LangGraph, Tool Calling | 9 |
| Observabilidade | LangSmith, RAGAS, loguru | 10 |
| DevOps | Docker, docker-compose, GitHub Actions | 11 |
| Cloud | Azure App Service ou Railway | 11 |
| MLOps/LLMOps | Prompt versioning, A/B testing | 12 |

---

## 📺 Canais e Recursos de Referência Rápida

| Canal / Recurso | Melhor para | Idioma |
|----------------|-------------|--------|
| Dunossauro YouTube | FastAPI, Python avançado | 🇧🇷 |
| Sandeco YouTube | LangChain, RAG, LLMs | 🇧🇷 |
| Código Fonte TV | Conceitos de IA | 🇧🇷 |
| Fabio Akita YouTube | Docker, infraestrutura | 🇧🇷 |
| Canal da Cloud | Azure em PT-BR | 🇧🇷 |
| LangChain YouTube (oficial) | LangChain, LangGraph | 🇺🇸 |
| James Briggs YouTube | RAG, embeddings | 🇺🇸 |
| ArjanCodes YouTube | Python profissional | 🇺🇸 |
| Sam Witteveen YouTube | LangChain, LLMs | 🇺🇸 |
| AI Jason YouTube | Agentes, automação | 🇺🇸 |
| Andrej Karpathy YouTube | Fundamentos de LLMs | 🇺🇸 |
| fastapidozero.dunossauro.com | FastAPI do zero | 🇧🇷 |
| promptingguide.ai/pt | Prompt engineering | 🇧🇷 |
| cookbook.openai.com | OpenAI na prática | 🇺🇸 |

---

*Cronograma v2 — Project-Based Learning | UaiFestas como produto central*
*Stack: FastAPI · Pydantic · SQLAlchemy · Pandas · OpenAI API · LangChain · ChromaDB · FAISS · RAG · LangGraph · LangSmith · RAGAS · Docker · CI/CD · Azure · MLOps*