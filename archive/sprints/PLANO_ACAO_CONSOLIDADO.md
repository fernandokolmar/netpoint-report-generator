# 🎯 PLANO DE AÇÃO CONSOLIDADO - PRSA Report Generator

**Projeto**: Gerador de Relatórios PRSA - Vale S.A.
**Data de Criação**: 29/01/2025
**Time**: Tech Lead, Backend Dev, Frontend Dev, QA, Data Analyst, Code Reviewer, Product Owner

---

## 📊 ANÁLISE EXECUTIVA

### Status Atual
- **Qualidade Geral**: ⭐⭐⭐⭐☆ (4/5)
- **Situação**: ✅ FUNCIONAL mas com riscos de integridade de dados
- **Recomendação**: 🟠 APROVAR COM REFATORAÇÃO OBRIGATÓRIA

### Resumo dos Problemas Identificados

| Área | Nota | Problemas Críticos | Ação |
|------|------|-------------------|------|
| **Arquitetura** | 6/10 | God Object, Acoplamento UI-Lógica | Refatorar em 5 classes |
| **Backend** | 6.5/10 | Cálculo errado, Performance lenta | Vetorização, validação |
| **Frontend** | 5/10 | UI trava, sem feedback visual | Threading, barra progresso |
| **QA** | 0/10 | Sem testes, bugs não detectados | Criar suite de testes |
| **Dados** | 6/10 | Tempo médio errado, duplicatas | Validação avançada |
| **Code Review** | - | 7 bloqueantes identificados | Corrigir antes de merge |
| **Negócio** | 4/5 | Validação insuficiente | Pré-visualização, alertas |

### ROI Esperado
- **Investimento**: 6 semanas (3 sprints)
- **Retorno**: -80% erros, +95% confiança, +40% adoção
- **Break-even**: 3 meses

---

## 🚀 ROADMAP DE 3 SPRINTS

### 📅 Timeline

```
Sprint 1: CRÍTICO        Sprint 2: IMPORTANTE    Sprint 3: MELHORIAS
(2 semanas)              (2 semanas)             (2 semanas)
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Confiabilidade│  →    │  Usabilidade  │  →    │   Insights    │
│   Integridade │       │   Qualidade   │       │  Estratégicos │
└───────────────┘       └───────────────┘       └───────────────┘
```

---

## 🔴 SPRINT 1: CRÍTICO (2 semanas)

**Objetivo**: Garantir confiabilidade e integridade de dados

**Meta**: ROI -80% erros de usuário, +30% confiança nos dados

### 📋 Backlog Sprint 1

| # | Tarefa | Prioridade | Esforço | Responsável | RICE |
|---|--------|-----------|---------|-------------|------|
| 1 | Separar classes (God Object → 5 classes) | 🔴 Crítica | 3 dias | Tech Lead | 54.0 |
| 2 | Desacoplar UI da lógica (callbacks) | 🔴 Crítica | 2 dias | Tech Lead | 71.3 |
| 3 | Validação avançada de dados | 🔴 Crítica | 2 dias | Backend + Data | 54.0 |
| 4 | Tratamento de erros específicos | 🔴 Crítica | 1.5 dias | Backend | 71.3 |
| 5 | Adicionar type hints em todas funções | 🔴 Crítica | 1 dia | Code Reviewer | - |
| 6 | Adicionar docstrings em todos métodos | 🔴 Crítica | 1 dia | Code Reviewer | - |
| 7 | Corrigir bug: tempo médio (fórmula Excel) | 🔴 Crítica | 0.5 dia | Data Analyst | - |
| 8 | Corrigir bug: validação CSV vazio | 🔴 Crítica | 0.5 dia | Backend | - |
| 9 | Threading + barra de progresso | 🔴 Crítica | 1.5 dias | Frontend | 53.3 |
| 10 | Eliminar duplicação código (DRY) | 🔴 Crítica | 1 dia | Backend | - |

**Total**: ~14 dias de esforço (distribuído em 2 semanas com time)

### 🎯 Critérios de Aceitação - Sprint 1

#### 1. Separação de Classes
```
✅ Criar classe ReportDataProcessor (lógica pura)
✅ Criar classe CSVLoader (carregamento de dados)
✅ Criar classe ExcelGenerator (geração de Excel)
✅ Criar classe ReportController (orquestração)
✅ Refatorar VideoConferenceReportGenerator (apenas UI)
✅ Todos os testes passam após refatoração
```

#### 2. Validação Avançada de Dados
```
✅ Validar CSV não vazio (erro descritivo)
✅ Validar colunas obrigatórias presentes
✅ Validar formato de datas
✅ Validar formato de celular (10-11 dígitos)
✅ Detectar valores nulos em campos críticos (com log)
✅ Validar range de valores (ex: usuários >= 0)
✅ Mensagens de erro específicas e acionáveis
```

#### 3. Threading + Barra de Progresso
```
✅ Processamento em thread separada (não trava UI)
✅ Barra de progresso indeterminada durante carregamento
✅ Progresso determinado (0% → 25% → 50% → 75% → 100%)
✅ Botão "Cancelar" funcional durante processamento
✅ Logs atualizados em tempo real mesmo com threading
```

#### 4. Tratamento de Erros
```
✅ Substituir TODOS os `except:` por exceções específicas
✅ FileNotFoundError com mensagem clara
✅ UnicodeDecodeError com sugestão de encoding
✅ pd.errors.EmptyDataError com arquivo identificado
✅ KeyError com coluna faltante especificada
✅ ValueError com causa e solução sugerida
✅ Logging estruturado em arquivo (.log)
```

#### 5. Bugs Críticos Corrigidos
```
✅ Tempo médio: adicionar coluna numérica auxiliar + fórmula AVERAGE correta
✅ CSV vazio: validação antes de processar
✅ Data inicial > final: validação e erro descritivo
✅ Fórmulas Excel: validar existência de colunas antes de gerar
```

### 📈 Métricas de Sucesso - Sprint 1

| Métrica | Antes | Meta Sprint 1 | Como Medir |
|---------|-------|---------------|------------|
| Taxa de erro | 0.2% | <0.05% | Logs de produção |
| Erros de validação detectados | 0% | >90% | Alertas antes de processar |
| Tempo para corrigir erro usuário | ~15min | <5min | Análise de sessões |
| Satisfação com mensagens erro | - | >7/10 | Survey pós-erro |
| Cobertura de testes | 0% | >40% | Coverage report |
| UI travada durante processamento | Sim | Não | Teste manual |

---

## 🟠 SPRINT 2: IMPORTANTE (2 semanas)

**Objetivo**: Melhorar usabilidade e qualidade de código

### 📋 Backlog Sprint 2

| # | Tarefa | Prioridade | Esforço | RICE |
|---|--------|-----------|---------|------|
| 11 | Pré-visualização de dados (primeiras 5 linhas) | 🟠 Alta | 1.5 dias | 53.3 |
| 12 | Detecção de duplicatas (Celular/Email) | 🟠 Alta | 2 dias | 28.0 |
| 13 | Exportação para PDF | 🟠 Alta | 4 dias | 21.0 |
| 14 | Indicadores visuais UI (✅/⚪ por arquivo) | 🟠 Alta | 1 dia | - |
| 15 | Log com cores por severidade (erro/sucesso/aviso) | 🟠 Alta | 0.5 dia | - |
| 16 | Atalhos de teclado (Ctrl+G, Ctrl+L, F1) | 🟠 Alta | 0.5 dia | - |
| 17 | Logging estruturado em arquivo | 🟠 Alta | 1 dia | - |
| 18 | Testes unitários (cobertura 40% → 80%) | 🟠 Alta | 3 dias | - |
| 19 | Filtros por Comunidade (já existe, documentar) | 🟠 Alta | 0.5 dia | 54.0 |

**Total**: ~14 dias de esforço

### 🎯 Critérios de Aceitação - Sprint 2

#### Pré-visualização de Dados
```
✅ Tabela mostrando primeiras 5 linhas de cada CSV carregado
✅ Contador de registros visível (ex: "1.631 registros")
✅ Preview atualizado ao carregar novo arquivo
✅ Botão "Ver Dados Completos" (opcional)
```

#### Detecção de Duplicatas
```
✅ Detectar duplicatas por Celular
✅ Alertar usuário: "5 celulares duplicados encontrados"
✅ Opção: "Remover Duplicatas" ou "Manter Todos"
✅ Log detalhado de duplicatas removidas
```

#### Exportação PDF
```
✅ Botão "Exportar para PDF" na interface
✅ PDF contém: Resumo executivo + Gráfico + Tabelas principais
✅ Formatação profissional (header com logo)
✅ Tempo de exportação <30s para relatórios médios
```

---

## 🟡 SPRINT 3: MELHORIAS (2 semanas)

**Objetivo**: Insights estratégicos e análises avançadas

### 📋 Backlog Sprint 3

| # | Tarefa | Prioridade | Esforço | RICE |
|---|--------|-----------|---------|------|
| 20 | Comparação entre múltiplos eventos | 🟡 Média | 5 dias | 7.2 |
| 21 | Histórico de relatórios gerados | 🟡 Média | 2.5 dias | 16.0 |
| 22 | Métricas adicionais (taxa participação, engajamento) | 🟡 Média | 2 dias | - |
| 23 | Top 5 Municípios/Comunidades | 🟡 Média | 1.5 dias | - |
| 24 | Curva de retenção (% do pico ao longo do tempo) | 🟡 Média | 1 dia | - |
| 25 | Menu bar profissional | 🟡 Baixa | 1 dia | - |
| 26 | Configuração persistente (último diretório) | 🟡 Baixa | 1 dia | - |

**Total**: ~14 dias de esforço

---

## 📁 ESTRUTURA DE ARQUIVOS PROPOSTA

### Após Refatoração (Sprint 1)

```
App Estatisticas/
├── prsa_report_generator.py       # UI apenas (Tkinter)
├── core/
│   ├── __init__.py
│   ├── controller.py               # ReportController (orquestração)
│   ├── data_loader.py              # CSVLoader (carregar CSVs)
│   ├── data_processor.py           # ReportDataProcessor (transformações)
│   ├── excel_generator.py          # ExcelGenerator (criar Excel)
│   ├── validators.py               # Validações de dados
│   └── exceptions.py               # Exceções customizadas
├── config/
│   ├── __init__.py
│   ├── settings.py                 # Constantes e configurações
│   └── column_mappings.py          # Mapeamentos de colunas
├── utils/
│   ├── __init__.py
│   ├── time_calculator.py          # Cálculos de tempo/retenção
│   └── logger.py                   # Logging estruturado
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_data_processor.py
│   ├── test_excel_generator.py
│   ├── test_validators.py
│   └── test_time_calculator.py
├── docs/                           # Já existe
├── agents/                         # Já existe
├── sprints/
│   ├── PLANO_ACAO_CONSOLIDADO.md  # Este arquivo
│   ├── SPRINT_1_TAREFAS.md
│   ├── SPRINT_2_TAREFAS.md
│   └── SPRINT_3_TAREFAS.md
├── logs/
│   └── prsa_report_*.log          # Logs gerados
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔧 TECNOLOGIAS E FERRAMENTAS

### Novas Dependências (Sprint 1-3)

```txt
# requirements.txt - Adicionar:

# Testes
pytest>=7.4.0
pytest-cov>=4.1.0
coverage>=7.3.0

# Logging
python-json-logger>=2.0.7

# PDF (Sprint 2)
reportlab>=4.0.0
# ou
pdfkit>=1.0.0

# Type checking
mypy>=1.7.0
```

### Ferramentas de Qualidade

```bash
# Cobertura de testes
pytest tests/ --cov=core --cov-report=html

# Type checking
mypy core/ --strict

# Linting
pylint core/

# Formatação
black core/ --line-length 100
```

---

## 📊 DEFINIÇÃO DE PRONTO (DoD)

### Para cada User Story

- [ ] Código implementado e funcionando
- [ ] Type hints em todas as funções
- [ ] Docstrings em todas as funções públicas
- [ ] Testes unitários escritos (quando aplicável)
- [ ] Testes passando (100%)
- [ ] Code review aprovado
- [ ] Documentação atualizada (README, docs/)
- [ ] Testado manualmente pelo PO
- [ ] Sem regressões (funcionalidades antigas funcionam)
- [ ] Commit com mensagem descritiva (Conventional Commits)

---

## 🎯 OBJETIVOS E KEY RESULTS (OKRs)

### Objetivo 1: Garantir Confiabilidade (Sprint 1)
- **KR1**: Reduzir taxa de erro de 0.2% para <0.05%
- **KR2**: 90% dos erros detectados ANTES de processar (validação)
- **KR3**: 100% das funções críticas com testes unitários
- **KR4**: 0 ocorrências de UI travada durante processamento

### Objetivo 2: Melhorar Experiência do Usuário (Sprint 2)
- **KR1**: Tempo para corrigir erro de 15min → <5min
- **KR2**: NPS de satisfação >9/10
- **KR3**: 80% de cobertura de testes
- **KR4**: 100% dos relatórios exportáveis em PDF

### Objetivo 3: Entregar Insights Estratégicos (Sprint 3)
- **KR1**: 80% dos usuários usando comparação entre eventos
- **KR2**: 5 novas métricas disponíveis
- **KR3**: 100% dos relatórios com análise de tendências
- **KR4**: Tempo de análise de múltiplos eventos <2min

---

## 👥 PAPÉIS E RESPONSABILIDADES

| Papel | Responsável | Principais Atividades |
|-------|-------------|----------------------|
| **Tech Lead** | - | Arquitetura, refatoração, code review |
| **Backend Dev** | - | Lógica de negócio, performance, validações |
| **Frontend Dev** | - | UI/UX, threading, indicadores visuais |
| **QA Engineer** | - | Testes, validação, detecção de bugs |
| **Data Analyst** | - | Métricas, fórmulas Excel, integridade dados |
| **Code Reviewer** | - | Padrões, qualidade código, documentação |
| **Product Owner** | - | Priorização, validação, aceite |

---

## 📅 CRONOGRAMA

```
Semana 1-2: Sprint 1 (CRÍTICO)
├── Dia 1-2: Refatoração arquitetura (separar classes)
├── Dia 3-4: Validações avançadas + tratamento erros
├── Dia 5-6: Threading + barra progresso
├── Dia 7-8: Eliminar duplicações (DRY)
├── Dia 9-10: Type hints, docstrings, testes básicos
└── Review + Ajustes

Semana 3-4: Sprint 2 (IMPORTANTE)
├── Dia 1-2: Pré-visualização + detecção duplicatas
├── Dia 3-6: Exportação PDF
├── Dia 7-8: Melhorias UI (indicadores, logs coloridos)
├── Dia 9-10: Testes unitários (40% → 80%)
└── Review + Ajustes

Semana 5-6: Sprint 3 (MELHORIAS)
├── Dia 1-3: Comparação entre eventos
├── Dia 4-5: Histórico de relatórios
├── Dia 6-7: Métricas adicionais
├── Dia 8-9: Top 5 Municípios/Comunidades
├── Dia 10: Polimento final
└── Review + Deploy
```

---

## 🚨 RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Refatoração quebra funcionalidades | Média | Alto | Testes de regressão após cada mudança |
| Threading introduz race conditions | Baixa | Alto | Testes específicos de concorrência |
| Exportação PDF muito lenta | Média | Médio | Implementar cache, otimizar imagens |
| Equipe sem conhecimento de arquitetura | Baixa | Alto | Pair programming, documentação detalhada |
| Scope creep (requisitos novos) | Alta | Médio | PO firme em manter escopo, backlog para futuro |
| Bugs em produção durante refatoração | Média | Alto | Deploy gradual, feature flags |

---

## 📞 COMUNICAÇÃO

### Daily Standup (Diário - 15min)
- O que fiz ontem?
- O que vou fazer hoje?
- Há bloqueios?

### Sprint Planning (Início de cada sprint)
- Revisar backlog
- Estimar esforço
- Definir metas da sprint

### Sprint Review (Fim de cada sprint)
- Demo das funcionalidades
- Feedback do PO
- Aceite das entregas

### Sprint Retrospective (Fim de cada sprint)
- O que funcionou bem?
- O que pode melhorar?
- Ações para próxima sprint

---

## ✅ APROVAÇÃO

Este plano foi revisado e aprovado por:

- [ ] **Tech Lead** - Arquitetura viável
- [ ] **Backend Developer** - Implementação factível
- [ ] **Frontend Developer** - UI/UX adequada
- [ ] **QA Engineer** - Testável
- [ ] **Data Analyst** - Métricas corretas
- [ ] **Code Reviewer** - Padrões de qualidade
- [ ] **Product Owner** - Valor de negócio validado

**Data de Aprovação**: ___/___/_____
**Início Oficial**: Sprint 1 - ___/___/_____

---

## 📚 REFERÊNCIAS

- [GUIDELINES.md](../docs/GUIDELINES.md) - Padrões de código
- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - Arquitetura do sistema
- [API_REFERENCE.md](../docs/API_REFERENCE.md) - Referência técnica
- [Análise Completa do Time](../docs/ANALISE_TIME_COMPLETA.md) - Diagnóstico detalhado

---

**Documento vivo**: Este plano será atualizado conforme necessário durante a execução.

**Última atualização**: 29/01/2025
