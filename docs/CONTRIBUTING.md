# 🤝 Guia de Contribuição - Gerador de Relatórios PRSA

Guia completo para contribuir com o desenvolvimento do projeto.

---

## 📋 Índice

- [Como Contribuir](#-como-contribuir)
- [Processo de Desenvolvimento](#-processo-de-desenvolvimento)
- [Reportar Bugs](#-reportar-bugs)
- [Sugerir Melhorias](#-sugerir-melhorias)
- [Pull Requests](#-pull-requests)
- [Padrões de Código](#-padrões-de-código)
- [Testes](#-testes)

---

## 🎯 Como Contribuir

Existem várias formas de contribuir com o projeto:

1. 🐛 **Reportar bugs** - Encontrou um problema? Reporte!
2. 💡 **Sugerir melhorias** - Tem uma ideia para melhorar o sistema?
3. 📝 **Melhorar documentação** - Documentação sempre pode ser melhorada
4. 🔧 **Corrigir bugs** - Resolva issues abertas
5. ✨ **Adicionar funcionalidades** - Implemente novos recursos
6. 🧪 **Escrever testes** - Aumente a cobertura de testes

---

## 🔄 Processo de Desenvolvimento

### 1. Configuração do Ambiente

```bash
# 1. Clone o repositório (se aplicável)
git clone <url-do-repositorio>
cd App\ Estatisticas

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Instale dependências de desenvolvimento (se houver)
pip install pytest black flake8 mypy
```

### 2. Workflow de Desenvolvimento

```
┌─────────────────────────────────────────────┐
│ 1. Escolher ou criar uma issue              │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 2. Criar branch feature/fix                 │
│    git checkout -b feature/minha-feature    │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 3. Desenvolver e testar localmente          │
│    - Escrever código                        │
│    - Escrever testes                        │
│    - Rodar testes                           │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 4. Commit seguindo convenções               │
│    git commit -m "feat: descrição"          │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 5. Push para repositório                    │
│    git push origin feature/minha-feature    │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 6. Criar Pull Request                       │
│    - Descrever mudanças                     │
│    - Referenciar issue                      │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 7. Code Review                              │
│    - Aguardar revisão                       │
│    - Aplicar feedback                       │
└──────────────┬──────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│ 8. Merge para main/develop                  │
└─────────────────────────────────────────────┘
```

### 3. Estrutura de Branches

```
main (produção)
  └── develop (desenvolvimento)
        ├── feature/adicionar-export-pdf
        ├── feature/melhorar-validacao-dados
        ├── fix/corrigir-calculo-retencao
        └── hotfix/corrigir-crash-inicializacao
```

**Convenções de Nomes**:
- `feature/` - Novas funcionalidades
- `fix/` - Correções de bugs
- `hotfix/` - Correções urgentes em produção
- `docs/` - Alterações em documentação
- `refactor/` - Refatoração de código
- `test/` - Adicionar/modificar testes

---

## 🐛 Reportar Bugs

### Template de Reporte de Bug

```markdown
## Descrição do Bug
[Descrição clara e concisa do bug]

## Passos para Reproduzir
1. Abrir aplicação
2. Carregar arquivo X
3. Clicar em Y
4. Ver erro

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que realmente acontece]

## Screenshots
[Se aplicável, adicione screenshots]

## Ambiente
- OS: [ex: Windows 10, Ubuntu 20.04]
- Python: [ex: 3.8.10]
- Versão do Projeto: [ex: 1.0.0]

## Logs de Erro
```
[Cole aqui o traceback completo]
```

## Dados de Exemplo
[Se possível, anexe arquivo CSV de exemplo que causa o erro]

## Informações Adicionais
[Qualquer contexto adicional]
```

### Exemplo de Bom Reporte

```markdown
## Descrição do Bug
Aplicação trava ao processar arquivo Inscritos.csv com mais de 10.000 linhas

## Passos para Reproduzir
1. Abrir prsa_report_generator.py
2. Carregar Inscritos.csv com 15.000 linhas
3. Clicar em "Processar e Gerar Relatório"
4. Interface congela e não responde

## Comportamento Esperado
Deveria processar arquivo e gerar Excel, mesmo com muitas linhas

## Comportamento Atual
Interface congela após ~5 segundos sem resposta

## Ambiente
- OS: Windows 11 Pro
- Python: 3.10.8
- pandas: 2.0.3
- RAM disponível: 8 GB

## Logs de Erro
Nenhum erro no console, aplicação simplesmente congela.

## Dados de Exemplo
Arquivo Inscritos.csv com 15.000 linhas (anexo)

## Informações Adicionais
Problema não ocorre com arquivos < 5.000 linhas
```

---

## 💡 Sugerir Melhorias

### Template de Sugestão de Feature

```markdown
## Descrição da Feature
[Descrição clara da funcionalidade desejada]

## Motivação
[Por que esta feature é importante?]

## Proposta de Solução
[Como você imagina que funcionaria?]

## Alternativas Consideradas
[Outras formas de resolver o problema]

## Impacto
- Usuários afetados: [ex: todos, apenas analistas, etc.]
- Complexidade estimada: [baixa/média/alta]
- Prioridade: [baixa/média/alta]

## Exemplos/Mockups
[Se possível, adicione exemplos visuais ou de código]
```

### Exemplo de Boa Sugestão

```markdown
## Descrição da Feature
Adicionar exportação para formato PDF além de Excel

## Motivação
Usuários frequentemente precisam compartilhar relatórios com pessoas
que não têm Excel instalado. PDF seria mais universal e imutável.

## Proposta de Solução
1. Adicionar botão "Exportar para PDF" na interface
2. Usar biblioteca reportlab para gerar PDF
3. Incluir as mesmas informações do Excel:
   - Tabelas de dados
   - Gráfico de retenção
   - Resumo estatístico

## Alternativas Consideradas
- Usar Excel → Salvar como PDF (mas requer Excel instalado)
- Gerar HTML → Imprimir como PDF (menos controle de layout)

## Impacto
- Usuários afetados: Todos
- Complexidade estimada: Média (nova dependência + layout)
- Prioridade: Média

## Exemplos/Mockups
[Mockup de layout do PDF]
```

---

## 🔀 Pull Requests

### Checklist Antes de Criar PR

- [ ] Código segue [GUIDELINES.md](GUIDELINES.md)
- [ ] Testes passam (se houver)
- [ ] Documentação atualizada (se aplicável)
- [ ] Commit messages seguem convenção
- [ ] Branch está atualizada com develop/main
- [ ] Código foi testado localmente
- [ ] Sem prints de debug esquecidos
- [ ] Imports estão organizados

### Template de Pull Request

```markdown
## Descrição
[Descrição clara das mudanças]

## Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação
- [ ] Refatoração (sem mudança de comportamento)

## Issues Relacionadas
Closes #[número da issue]

## Como Testar
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Screenshots (se aplicável)
[Adicione screenshots]

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Documentação atualizada
- [ ] Testes adicionados/atualizados
- [ ] Commits seguem convenção
- [ ] Testado localmente

## Notas Adicionais
[Informações extras para reviewers]
```

### Exemplo de Bom Pull Request

```markdown
## Descrição
Adiciona validação de tamanho de arquivo antes de processar CSVs

## Tipo de Mudança
- [x] Nova feature
- [x] Bug fix (evita crash com arquivos grandes)

## Issues Relacionadas
Closes #42

## Mudanças Implementadas
1. Verificação de tamanho de arquivo em `load_dataframes()`
2. Aviso ao usuário se arquivo > 100 MB
3. Opção de continuar ou cancelar processamento
4. Log do tamanho de cada arquivo carregado

## Como Testar
1. Abrir aplicação
2. Tentar carregar arquivo CSV > 100 MB
3. Verificar se aparece aviso
4. Confirmar que pode escolher continuar ou cancelar

## Screenshots
[Screenshot do aviso de tamanho de arquivo]

## Código Adicionado
```python
def validate_file_size(file_path, max_mb=100):
    size_mb = os.path.getsize(file_path) / (1024 * 1024)

    if size_mb > max_mb:
        result = messagebox.askyesno(
            "Arquivo Grande",
            f"Arquivo tem {size_mb:.1f} MB. Continuar?"
        )
        return result

    return True
```

## Checklist
- [x] Código segue GUIDELINES.md
- [x] Documentação atualizada (README.md)
- [x] Testado com arquivos de diferentes tamanhos
- [x] Commits seguem convenção

## Notas Adicionais
Considerei limite de 100 MB baseado em testes com máquinas de 8 GB RAM.
Pode ser configurável no futuro.
```

---

## 📏 Padrões de Código

### Seguir Diretrizes

Todo código deve seguir [GUIDELINES.md](GUIDELINES.md):

- ✅ PEP 8
- ✅ Type hints
- ✅ Docstrings
- ✅ Nomes descritivos
- ✅ Tratamento de erros adequado

### Formatação Automática

```bash
# Formatar com Black
black prsa_report_generator.py

# Verificar com flake8
flake8 prsa_report_generator.py

# Type checking com mypy
mypy prsa_report_generator.py
```

### Exemplo de Código Bem Formatado

```python
def process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados de inscritos.

    Args:
        df: DataFrame bruto de inscritos

    Returns:
        DataFrame processado com colunas padronizadas

    Raises:
        ValueError: Se DataFrame estiver vazio
        KeyError: Se colunas obrigatórias estiverem ausentes
    """
    # Validação de entrada
    if df.empty:
        raise ValueError("DataFrame de inscritos está vazio")

    # Renomear colunas
    if 'Login' in df.columns:
        df.rename(columns={'Login': 'Celular'}, inplace=True)

    # Selecionar colunas existentes
    colunas_desejadas = ['Nome', 'Celular', 'Município', 'Comunidade']
    colunas_existentes = [col for col in colunas_desejadas if col in df.columns]

    return df[colunas_existentes]
```

---

## 🧪 Testes

### Escrever Testes

```python
import unittest
import pandas as pd
from prsa_report_generator import VideoConferenceReportGenerator

class TestProcessInscritos(unittest.TestCase):
    """Testes para process_inscritos."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.app = VideoConferenceReportGenerator(None)

    def test_renomeia_login_para_celular(self):
        """Testa se Login é renomeado para Celular."""
        df = pd.DataFrame({
            'Nome': ['João', 'Maria'],
            'Login': ['31999999999', '21988888888']
        })

        resultado = self.app.process_inscritos(df)

        self.assertIn('Celular', resultado.columns)
        self.assertNotIn('Login', resultado.columns)

    def test_levanta_erro_dataframe_vazio(self):
        """Testa se ValueError é levantado para DataFrame vazio."""
        df_vazio = pd.DataFrame()

        with self.assertRaises(ValueError):
            self.app.process_inscritos(df_vazio)

    def test_mantem_apenas_colunas_existentes(self):
        """Testa se seleciona apenas colunas que existem."""
        df = pd.DataFrame({
            'Nome': ['João'],
            'Login': ['31999999999']
            # Sem Município, Comunidade, etc.
        })

        resultado = self.app.process_inscritos(df)

        # Deve ter apenas Nome e Celular
        self.assertEqual(len(resultado.columns), 2)

if __name__ == '__main__':
    unittest.main()
```

### Rodar Testes

```bash
# Rodar todos os testes
python -m unittest discover

# Rodar teste específico
python test_prsa.py

# Rodar com coverage
pip install coverage
coverage run -m unittest discover
coverage report
coverage html  # Gera relatório HTML
```

---

## 🔍 Code Review

### O que Reviewers Verificam

1. **Funcionalidade**
   - Código faz o que deveria?
   - Casos extremos tratados?

2. **Qualidade**
   - Segue padrões do projeto?
   - Código é legível?
   - Há duplicação?

3. **Testes**
   - Testes cobrem mudanças?
   - Testes passam?

4. **Documentação**
   - Docstrings presentes?
   - README atualizado?
   - CHANGELOG atualizado (se houver)?

5. **Performance**
   - Mudanças impactam performance?
   - Há otimizações necessárias?

### Como Dar Bom Feedback

```markdown
# ❌ Feedback Ruim
"Esse código está horrível"

# ✅ Feedback Bom
"Sugestão: Esta função poderia ser refatorada para melhorar legibilidade.
Em vez de:
```python
if x:
    if y:
        if z:
            return True
```
Considere:
```python
return x and y and z
```"
```

---

## 📝 Commit Messages

### Formato

```
tipo(escopo): descrição curta (máx 50 chars)

Descrição detalhada opcional (máx 72 chars por linha).
Explique o "por quê" e não o "o quê".

Rodapé opcional (refs, closes, breaking changes).
```

### Tipos

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança lógica)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas (build, dependências)

### Exemplos

```bash
# Feature
git commit -m "feat(excel): adicionar exportação para PDF"

# Bug fix
git commit -m "fix(csv): corrigir encoding para arquivos com acentos"

# Documentação
git commit -m "docs(readme): atualizar seção de instalação"

# Refatoração
git commit -m "refactor(process): simplificar cálculo de retenção"

# Com corpo e rodapé
git commit -m "feat(validacao): adicionar validação de tamanho de arquivo

Implementa verificação de tamanho antes de carregar CSV.
Usuário é avisado se arquivo > 100 MB e pode cancelar.

Closes #42"
```

---

## 🎯 Priorização de Issues

### Níveis de Prioridade

| Prioridade | Descrição | Tempo Esperado |
|-----------|-----------|----------------|
| **🔴 Crítico** | Sistema não funciona | Imediato |
| **🟠 Alto** | Funcionalidade importante quebrada | 1-3 dias |
| **🟡 Médio** | Bug que tem workaround | 1-2 semanas |
| **🟢 Baixo** | Melhoria, não urgente | Quando possível |

### Labels Sugeridas

- `bug` - Algo não funciona
- `enhancement` - Nova feature
- `documentation` - Melhoria de docs
- `good first issue` - Bom para iniciantes
- `help wanted` - Precisa de ajuda
- `question` - Pergunta/discussão

---

## 📜 Licença e Propriedade Intelectual

**Importante**: Este projeto é propriedade da Vale S.A.

Ao contribuir, você concorda que:
- Suas contribuições se tornam propriedade da Vale S.A.
- Suas contribuições podem ser usadas internamente
- Você tem direito de fazer essas contribuições

---

## 🙏 Agradecimentos

Obrigado por contribuir para o projeto! Sua ajuda é muito apreciada.

Principais contribuidores serão reconhecidos no README principal.

---

## 📞 Dúvidas?

Se tiver dúvidas sobre como contribuir:

1. Leia esta documentação completa
2. Consulte [GUIDELINES.md](GUIDELINES.md)
3. Verifique issues existentes
4. Entre em contato com a equipe de desenvolvimento

---

**Documento mantido por**: Equipe de Desenvolvimento PRSA
**Última atualização**: 29/01/2025
