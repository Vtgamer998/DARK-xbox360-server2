# Guia de Integração Stealth Server (Xbox 360)

Este backend fornece a API necessária para o seu plugin `.xex` se comunicar com o servidor.

## Endpoints da API

### 1. Autenticação
- **URL:** `https://seu-servidor.pythonanywhere.com/api/v1/auth`
- **Método:** `POST`
- **Corpo (JSON):**
```json
{
    "cpukey": "SUA_CPU_KEY_AQUI"
}
```

### 2. Desafios (Challenges)
- **URL:** `https://seu-servidor.pythonanywhere.com/api/v1/challenges`
- **Método:** `GET`
- **Resposta:** Retorna os dados necessários para o bypass da Xbox Live.

## Como usar no Plugin (.xex)
Você deve configurar seu código C++ no Xbox para fazer requisições HTTP para estes endpoints. O servidor irá validar a CPU Key e retornar se o console está autorizado a usar o serviço furtivo.

## Painel de Controle
Acesse a URL principal do seu servidor no navegador para gerenciar os consoles conectados, banir usuários ou alterar a versão do sistema.
