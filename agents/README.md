# 🤖 Agentes de IA - Time de Desenvolvimento PRSA

Bem-vindo ao time de agentes especializados para desenvolvimento do **Gerador de Relatórios PRSA**.

Esta pasta contém agentes de IA que simulam diferentes funções de um time de software profissional, cada um com suas responsabilidades, conhecimentos e contexto específico do projeto.

---

## 📋 Índice de Agentes

### 👔 Gestão e Produto

- **[PRODUCT_OWNER.md](PRODUCT_OWNER.md)** - Product Owner (PO)
  - Define requisitos e prioridades
  - Representa as necessidades dos stakeholders
  - Valida se entregas atendem aos objetivos de negócio

### 🏗️ Arquitetura e Liderança Técnica

- **[TECH_LEAD.md](TECH_LEAD.md)** - Tech Lead / Arquiteto de Software
  - Define arquitetura e padrões técnicos
  - Toma decisões de design
  - Revisa soluções de alto nível

### 💻 Desenvolvimento

- **[BACKEND_DEVELOPER.md](BACKEND_DEVELOPER.md)** - Backend Developer / Python Developer
  - Implementa lógica de negócio
  - Desenvolve processamento de dados
  - Cria integrações e APIs

- **[FRONTEND_DEVELOPER.md](FRONTEND_DEVELOPER.md)** - Frontend Developer / UI Developer
  - Desenvolve interface gráfica (Tkinter)
  - Implementa interações do usuário
  - Garante usabilidade

### 🧪 Qualidade

- **[QA_ENGINEER.md](QA_ENGINEER.md)** - QA Engineer / Tester
  - Cria planos de teste
  - Escreve testes automatizados
  - Valida qualidade e encontra bugs

- **[CODE_REVIEWER.md](CODE_REVIEWER.md)** - Code Reviewer / Senior Developer
  - Revisa pull requests
  - Garante qualidade de código
  - Verifica conformidade com padrões

### 🚀 Infraestrutura

- **[DEVOPS_ENGINEER.md](DEVOPS_ENGINEER.md)** - DevOps Engineer
  - Gerencia builds e deploys
  - Configura ambientes
  - Automatiza processos

### 📊 Dados

- **[DATA_ANALYST.md](DATA_ANALYST.md)** - Data Analyst / Business Intelligence
  - Analisa formatos de dados
  - Valida transformações
  - Define métricas e relatórios

### 📝 Documentação

- **[TECHNICAL_WRITER.md](TECHNICAL_WRITER.md)** - Technical Writer / Documentador
  - Escreve documentação técnica
  - Mantém README e guias
  - Cria tutoriais

---

## 🎯 Quando Usar Cada Agente

### Situações por Tipo de Tarefa

| Tarefa | Agente Recomendado | Por quê |
|--------|-------------------|---------|
| **Definir nova funcionalidade** | Product Owner | Entende requisitos de negócio |
| **Decidir arquitetura** | Tech Lead | Visão técnica de alto nível |
| **Implementar feature** | Backend Developer | Codifica lógica de negócio |
| **Melhorar interface** | Frontend Developer | Especialista em UI/UX |
| **Testar funcionalidade** | QA Engineer | Cria testes e valida qualidade |
| **Revisar código** | Code Reviewer | Garante padrões e boas práticas |
| **Configurar deploy** | DevOps Engineer | Automatiza infraestrutura |
| **Validar dados** | Data Analyst | Especialista em dados e métricas |
| **Escrever documentação** | Technical Writer | Comunica tecnicamente |

---

## 🔄 Fluxo de Trabalho com Agentes

### Exemplo: Adicionar Nova Feature

```
1. PRODUCT OWNER
   ├─ Define requisitos
   ├─ Prioriza feature
   └─ Cria user story
       ↓
2. TECH LEAD
   ├─ Analisa impacto arquitetural
   ├─ Define abordagem técnica
   └─ Aloca complexidade
       ↓
3. DATA ANALYST (se aplicável)
   ├─ Define formato de dados
   ├─ Valida transformações
   └─ Especifica métricas
       ↓
4. BACKEND DEVELOPER
   ├─ Implementa lógica
   ├─ Processa dados
   └─ Cria commits
       ↓
5. FRONTEND DEVELOPER
   ├─ Implementa UI
   ├─ Adiciona interações
   └─ Testa visualmente
       ↓
6. QA ENGINEER
   ├─ Escreve testes
   ├─ Executa validações
   └─ Reporta bugs
       ↓
7. CODE REVIEWER
   ├─ Revisa PR
   ├─ Valida padrões
   └─ Aprova/rejeita
       ↓
8. DEVOPS ENGINEER
   ├─ Configura build
   ├─ Faz deploy
   └─ Monitora
       ↓
9. TECHNICAL WRITER
   ├─ Atualiza docs
   ├─ Escreve changelog
   └─ Publica guia
```

---

## 💡 Como Usar os Agentes

### Formato de Prompt

Ao interagir com um agente, use este formato:

```markdown
# Contexto
[Descreva a situação atual do projeto]

# Tarefa
[O que você precisa que o agente faça]

# Restrições
[Limitações ou requisitos específicos]

# Resultado Esperado
[O que você espera receber como output]
```

### Exemplo Prático

```markdown
@BACKEND_DEVELOPER.md

# Contexto
O sistema atualmente gera relatórios apenas em Excel.
Usuários pediram exportação para PDF.

# Tarefa
Implementar função para exportar relatórios em formato PDF,
mantendo a mesma estrutura visual (tabelas + gráficos).

# Restrições
- Usar biblioteca reportlab
- Não quebrar funcionalidade existente de Excel
- Manter performance aceitável (<5s para gerar PDF)

# Resultado Esperado
- Código Python implementado
- Função exportar_para_pdf() funcional
- Testes unitários básicos
```

---

## 🧩 Combinando Agentes

### Cenário 1: Bug Crítico

```
1. QA_ENGINEER → Identifica e documenta bug
2. TECH_LEAD → Analisa causa raiz e impacto
3. BACKEND_DEVELOPER → Implementa correção
4. CODE_REVIEWER → Valida fix
5. DEVOPS_ENGINEER → Deploy hotfix
```

### Cenário 2: Refatoração

```
1. TECH_LEAD → Propõe refatoração
2. CODE_REVIEWER → Revisa proposta
3. BACKEND_DEVELOPER → Implementa mudanças
4. QA_ENGINEER → Testa regressão
5. TECHNICAL_WRITER → Atualiza docs
```

### Cenário 3: Nova Feature Completa

```
1. PRODUCT_OWNER → Define requisitos
2. DATA_ANALYST → Especifica dados
3. TECH_LEAD → Define arquitetura
4. BACKEND_DEVELOPER → Desenvolve backend
5. FRONTEND_DEVELOPER → Desenvolve UI
6. QA_ENGINEER → Testa end-to-end
7. CODE_REVIEWER → Revisa tudo
8. TECHNICAL_WRITER → Documenta
9. DEVOPS_ENGINEER → Faz deploy
```

---

## 📚 Conhecimento dos Agentes

Todos os agentes têm acesso à documentação do projeto:

- ✅ [Documentação técnica completa](../docs/README.md)
- ✅ [Arquitetura do sistema](../docs/ARCHITECTURE.md)
- ✅ [Diretrizes de código](../docs/GUIDELINES.md)
- ✅ [Formatos de dados](../docs/DATA_FORMATS.md)
- ✅ [API Reference](../docs/API_REFERENCE.md)
- ✅ [Troubleshooting](../docs/TROUBLESHOOTING.md)
- ✅ [Como contribuir](../docs/CONTRIBUTING.md)

---

## 🎭 Personalidade dos Agentes

Cada agente tem uma personalidade e estilo de comunicação específico:

| Agente | Estilo | Foco |
|--------|--------|------|
| **Product Owner** | Orientado a negócio, pergunta "por quê?" | Valor para usuário |
| **Tech Lead** | Visionário, estratégico | Arquitetura sustentável |
| **Backend Dev** | Pragmático, detalhista | Código que funciona |
| **Frontend Dev** | Criativo, user-centric | Experiência do usuário |
| **QA Engineer** | Cético, minucioso | Qualidade e edge cases |
| **Code Reviewer** | Crítico construtivo | Padrões e manutenibilidade |
| **DevOps** | Automatizador, sistemático | Confiabilidade |
| **Data Analyst** | Analítico, baseado em dados | Métricas e insights |
| **Tech Writer** | Claro, didático | Compreensão |

---

## 🚀 Exemplos de Uso

### Exemplo 1: Consultar Product Owner

```
Você: @PRODUCT_OWNER.md

Estou pensando em adicionar suporte para múltiplos idiomas
na interface. Isso faz sentido para os usuários do PRSA?

PO: Excelente pergunta! Vamos analisar:

CONTEXTO DE NEGÓCIO:
- Usuários são majoritariamente brasileiros (comunidades afetadas em MG)
- Vale atua em português
- Eventos de reparação são em português

ANÁLISE:
- Prioridade: BAIXA
- Esforço estimado: ALTO
- Valor para usuário: BAIXO (no momento)

RECOMENDAÇÃO:
Não priorizar agora. Focar em:
1. Estabilidade do sistema atual
2. Melhorias em relatórios existentes
3. Novas métricas solicitadas

Se houver mudança no escopo (Vale global), revisitamos.
```

### Exemplo 2: Consultar Tech Lead

```
Você: @TECH_LEAD.md

Preciso adicionar cache para evitar reprocessar CSVs grandes.
Qual abordagem você recomenda?

Tech Lead: Boa identificação do problema! Vamos arquitetar:

OPÇÕES:
1. Cache em memória (dict Python)
2. Cache em disco (pickle/joblib)
3. Banco de dados SQLite

ANÁLISE:
Opção 1 - Cache em Memória:
✅ Mais rápido
❌ Perdido ao fechar app
❌ Limitado pela RAM

Opção 2 - Cache em Disco:
✅ Persiste entre execuções
✅ Simples de implementar
⚠️ Precisa invalidar quando CSV muda

Opção 3 - SQLite:
✅ Estruturado
❌ Overhead para uso simples
❌ Mais complexo

RECOMENDAÇÃO:
Use Opção 2 (Cache em Disco) com joblib:

[código de exemplo...]

PRÓXIMOS PASSOS:
1. Implementar cache
2. Adicionar hash MD5 do arquivo
3. Invalidar se hash mudar
4. Testar com arquivos grandes
```

---

## 📊 Métricas de Uso dos Agentes

### Quando Escolher Cada Agente (%)

```
Product Owner      ████████░░ 40% - Requisitos, Priorização
Tech Lead          ███████░░░ 35% - Arquitetura, Decisões
Backend Dev        ██████████ 50% - Implementação
Frontend Dev       ████░░░░░░ 20% - UI (projeto simples)
QA Engineer        ██████░░░░ 30% - Testes, Validação
Code Reviewer      ████████░░ 40% - PRs, Padrões
DevOps             ███░░░░░░░ 15% - Deploy, CI/CD
Data Analyst       ██████░░░░ 30% - Dados, Métricas
Tech Writer        █████░░░░░ 25% - Documentação
```

---

## 🎯 Casos de Uso Rápidos

### "Preciso de ajuda com..."

| Necessidade | Use este agente |
|-------------|-----------------|
| Entender requisitos | Product Owner |
| Decidir tecnologia | Tech Lead |
| Escrever código Python | Backend Developer |
| Melhorar interface Tkinter | Frontend Developer |
| Criar testes | QA Engineer |
| Revisar PR | Code Reviewer |
| Automatizar build | DevOps Engineer |
| Validar CSV | Data Analyst |
| Escrever README | Technical Writer |

---

## 🔧 Personalização de Agentes

Você pode modificar os agentes para:
- ✅ Adicionar contexto específico do seu projeto
- ✅ Incluir preferências técnicas da equipe
- ✅ Ajustar tom e estilo de comunicação
- ✅ Adicionar ferramentas ou frameworks específicos

---

## 📝 Contribuindo com Novos Agentes

Para adicionar um novo agente:

1. Copie template de agente existente
2. Defina responsabilidades claras
3. Adicione contexto do projeto
4. Especifique conhecimentos técnicos
5. Crie exemplos de uso
6. Atualize este README

---

## 🆘 Suporte

Se não souber qual agente usar:

1. **Consulte a tabela "Quando Usar Cada Agente"** acima
2. **Leia os exemplos de uso** de cada agente
3. **Em caso de dúvida, comece com o Tech Lead** - ele pode direcionar para o agente correto

---

**Time de agentes desenvolvido para o projeto PRSA - Vale S.A.**

*Última atualização: 29/01/2025*
