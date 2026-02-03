# GUIA DE INSTALAÇÃO RÁPIDA - Gerador de Relatório PRSA

## 📋 Pré-requisitos
- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

## 🚀 Instalação Rápida

### Windows:
1. Baixe todos os arquivos para uma pasta
2. Dê duplo clique em `executar_windows.bat`
3. A aplicação será iniciada automaticamente

### Linux/Mac:
1. Baixe todos os arquivos para uma pasta
2. Abra o terminal na pasta
3. Execute: `./executar_linux_mac.sh`

### Instalação Manual (qualquer sistema):
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
python prsa_report_generator.py
```

## 📁 Arquivos Incluídos

- `prsa_report_generator.py` - Aplicação principal
- `requirements.txt` - Dependências Python
- `README.md` - Documentação completa
- `executar_windows.bat` - Script para Windows
- `executar_linux_mac.sh` - Script para Linux/Mac
- `test_prsa.py` - Script de teste (opcional)
- `INSTALACAO_RAPIDA.md` - Este arquivo

## 💡 Dicas

- Certifique-se de que os arquivos CSV estão em UTF-8
- Use ponto e vírgula (;) como separador nos CSVs
- O arquivo Excel gerado terá gráficos e tabelas dinâmicas
- Salve o relatório com um nome descritivo incluindo a data

## ❓ Problemas Comuns

**Python não encontrado:**
- Baixe e instale: https://www.python.org/downloads/

**Erro ao instalar dependências:**
- Execute como administrador (Windows)
- Use `sudo` no Linux/Mac

**Interface não aparece:**
- Verifique se o Python tem suporte a Tkinter
- No Linux: `sudo apt-get install python3-tk`

## 📞 Suporte
Em caso de dúvidas, consulte o README.md completo ou contacte a equipe técnica.
