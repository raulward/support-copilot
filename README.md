Perfeito — você está certo nos dois pontos:
	1.	Docker + pgvector precisam estar documentados no README
	2.	A API deve sim aparecer no docker-compose (mesmo que opcional)

Abaixo está o README corrigido, completo e profissional, já incluindo Docker + pgvector + API no compose, pronto apenas para copiar e colar.

⸻


# Support Copilot — RAG + Specialist LLM para Atendimento Técnico

Support Copilot é um serviço de backend que analisa mensagens de tickets de suporte e retorna respostas estruturadas e fundamentadas em uma base de conhecimento interna (KB), utilizando **Retrieval-Augmented Generation (RAG)** e um **LLM especialista**.

O projeto foi desenvolvido com foco em **engenharia de IA aplicada**, priorizando arquitetura limpa, explicabilidade, segurança e **reprodutibilidade de ambiente**.

---

## Objetivo do Projeto

Times de suporte técnico lidam diariamente com:
- triagem repetitiva de tickets
- perguntas de diagnóstico padronizadas
- procedimentos conhecidos (2FA, reset de senha, incidentes, integrações)
- risco de solicitar dados sensíveis indevidamente

Este projeto demonstra como um **copiloto de IA** pode:
- recuperar contexto relevante da KB
- gerar respostas **grounded** (sem alucinação)
- retornar JSON estruturado pronto para integração com sistemas de atendimento

---

## Funcionalidades

- Classificação de ticket (categoria, prioridade, confiança — MVP)
- Resumo do problema
- Perguntas de diagnóstico
- Ações sugeridas
- Resposta pronta para o usuário (`draft_reply`)
- Citações da base de conhecimento utilizada (RAG)
- Métricas básicas de uso e latência

---

## Arquitetura (Visão Geral)
```
FastAPI (API Layer)
|
v
Service Layer (orquestração)
|
+–> Router (heurístico - MVP)
|
+–> Retriever (pluggable)
|       - FAISS (local, MVP)
|       - pgvector (Postgres)
|
+–> Specialist LLM
- recebe ticket + contexto (KB)
- retorna JSON estruturado
```
---

## Componentes Principais

### 1. API (FastAPI)
Endpoint principal:

POST /ticket/analyze

Responsável por:
- receber o ticket
- delegar a análise para a camada de serviço
- retornar resposta estruturada em JSON

---

### 2. Service Layer
Responsável por orquestrar o fluxo completo:
- geração de `request_id`
- roteamento inicial (heurístico)
- recuperação de contexto (RAG)
- chamada ao Specialist LLM
- consolidação da resposta final

Essa camada **não contém lógica de IA diretamente**, apenas coordenação.

---

### 3. Base de Conhecimento (KB)
A KB é mantida em arquivos Markdown (`/kb`), com playbooks curtos e objetivos, por exemplo:
- `acesso_2fa.md`
- `seguranca_pii.md`
- `agendamento_conflitos.md`

Cada documento contém:
- quando usar
- sintomas comuns
- procedimento recomendado
- perguntas de diagnóstico
- critérios de escalonamento

---

### 4. Chunking e Ingest
- Documentos da KB são divididos em chunks com tamanho fixo + overlap
- Chunking simples, seguro e determinístico
- Artefatos gerados:
  - `data/kb_chunks.json`

Os chunks podem ser ingeridos:
- localmente (FAISS)
- ou no banco (Postgres + pgvector)

---

### 5. Retrieval (RAG)

#### Backend FAISS (MVP)
- Índice vetorial local
- Embeddings via OpenAI (`text-embedding-3-small`)
- Similaridade por cosseno
- Ideal para prototipação rápida

#### Backend Postgres + pgvector
- Persistência de embeddings
- Busca vetorial diretamente no banco
- Infraestrutura reproduzível via Docker
- Pronto para produção

A escolha do backend é feita via variável de ambiente:
```
RETRIEVER_BACKEND=faiss | pgvector
```
---

### 6. Specialist LLM
O LLM atua como um **especialista de suporte técnico**.

Características:
- recebe apenas o ticket e o contexto recuperado
- regras explícitas no prompt:
  - usar somente o contexto fornecido
  - não inventar procedimentos
  - fazer perguntas quando o contexto for insuficiente
  - nunca solicitar dados sensíveis (senha, 2FA, tokens)
- saída validada via **JSON Schema**

---

## Segurança e PII

O projeto inclui:
- KB específica para segurança e dados sensíveis
- regras explícitas no prompt do LLM
- prevenção de solicitações indevidas de informações críticas

---

## Como Executar Localmente

### Requisitos
- Python 3.11+
- Poetry
- Docker + Docker Compose

---

### Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=YOUR_API_KEY
RETRIEVER_BACKEND=pgvector
DATABASE_URL=postgresql+psycopg://support:support@postgres:5432/supportcopilot
```

---

## Subir infraestrutura (Postgres + pgvector)
```
docker compose up -d
```
O banco é criado automaticamente com:
	•	extensão pgvector
	•	tabela kb_chunks
	•	índice vetorial

### Scripts SQL ficam em:

```
db/init/
```

---

## Gerar chunks da KB

poetry run python scripts/ingest_kb.py


---

## Ingerir chunks no Postgres

poetry run python scripts/ingest_pgvector.py


---

## Subir a API (local ou via Docker)

### Local

poetry run uvicorn app.main:app --reload

### Via Docker (opcional)

A API também pode ser executada como serviço no docker-compose, garantindo ambiente totalmente reproduzível.

⸻

## Health Check

GET http://127.0.0.1:8000/health


---

## Exemplo de Uso

Request

{
  "ticket_id": "TCK-0001",
  "channel": "web",
  "message": "Não recebo o código 2FA por SMS e minha conta bloqueou."
}

Response

{
  "category": "Acesso/Conta",
  "priority": "P2",
  "summary": "...",
  "diagnostic_questions": [...],
  "suggested_actions": [...],
  "draft_reply": "...",
  "citations": [...]
}

---

## Estrutura do Projeto

app/
  api/            # Endpoints FastAPI
  services/       # Orquestração do fluxo
  rag/            # Retrieval (FAISS / pgvector)
  agents/         # Specialist LLM
  core/           # Schemas e logging
  db/             # Conexão e init SQL
kb/               # Base de conhecimento
scripts/          # Ingest KB e embeddings
data/             # Artefatos locais (FAISS)
docker-compose.yml
