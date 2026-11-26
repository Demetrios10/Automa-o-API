# QA API Automation — Python + Playwright + Pytest

[![API Tests](https://github.com/Demetrios10/Automa-o-API/actions/workflows/api-tests.yml/badge.svg)](https://github.com/Demetrios10/Automa-o-API/actions/workflows/api-tests.yml)

Framework demonstrativo de **automação de testes de API REST**, com boas práticas de QA Automation: HTTP client, fixtures, parametrização, testes positivos e negativos, validações de contrato JSON e integração contínua.

## Stack
Python 3.12 · Playwright (APIRequestContext) · Pytest · pytest-playwright · pytest-html · GitHub Actions.

## API
[JSONPlaceholder](https://jsonplaceholder.typicode.com/) — endpoints `/posts`. **POST, PUT, PATCH e DELETE são operações simuladas e não persistem alterações.** As assertions verificam apenas a resposta HTTP. A disponibilidade do serviço de terceiros pode afetar a pipeline.

## Executar
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```
Não é necessário instalar browser. Para smoke: `pytest -m smoke -v`.

Relatório:
```bash
pytest -v --html=report.html --self-contained-html --junitxml=report.xml
```

Configuração opcional: copie `.env.example` para `.env`. A configuração padrão usa a URL pública.

## Casos de teste
| Cenário | Validações |
|---|---|
| Listagem de posts | HTTP 200, lista e contrato |
| Consulta de 4 posts | HTTP 200, ID e campos |
| Filtro por usuário | HTTP 200 e userId |
| 2 IDs inexistentes | HTTP 404 e objeto vazio |
| Criação simulada | HTTP 201 e campos do payload |
| Substituição simulada | HTTP 200 e campos |
| Atualização parcial simulada | HTTP 200 e título |
| Exclusão simulada | HTTP 200 |

**12 execuções de testes parametrizadas**. Esta API não exige autenticação; não há validações fictícias de 401/403.

## Arquitetura
```text
clients/posts_client.py           Cliente HTTP e endpoints
tests/conftest.py                Fixtures
tests/test_posts_api.py          Cenários automatizados
.github/workflows/api-tests.yml  Pipeline CI
pytest.ini                       Markers
requirements.txt                 Dependências
.env.example                     Exemplo de variáveis
```

## Pipeline
GitHub Actions executa os testes a cada push, pull request ou acionamento manual. Relatórios HTML e JUnit são enviados como artefatos. Confira o status atual no badge acima; não pressupõe aprovação antes da execução.

## Evoluções planejadas
JSON Schema · API autenticada · Allure · testes de integração com dados isolados.

## Referências
[Playwright API Testing](https://playwright.dev/python/docs/api-testing) · [JSONPlaceholder](https://jsonplaceholder.typicode.com/guide/)

## Revisão e autoria

**Demétrios Alves da Silva** · QA Analyst · [Portfólio](https://github.com/Demetrios10/Demetrios10/blob/main/PORTFOLIO.md) · [LinkedIn](https://www.linkedin.com/in/demetriosalvess)
