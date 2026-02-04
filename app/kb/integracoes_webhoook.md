# Integrações via Webhook e APIs

## Quando usar
- Quando o cliente relata que dados não estão sincronizando.
- Quando eventos não chegam ao sistema integrado.
- Quando há erro ao configurar webhook ou endpoint.
- Quando há dúvidas sobre autenticação ou formato de payload.

## Sintomas comuns
- “O webhook não dispara.”
- “Os dados não chegam no sistema.”
- “Recebo erro 401/403 no webhook.”
- “O endpoint retorna erro 500.”
- “A integração funcionava e parou.”

## Procedimento
1. Confirmar o endpoint configurado:
   - URL correta
   - método HTTP esperado (POST/PUT)
2. Validar autenticação:
   - token/chave configurada corretamente
   - token não expirado ou revogado
3. Verificar formato do payload:
   - campos obrigatórios
   - tipo de conteúdo (JSON)
4. Testar o endpoint manualmente (ex.: curl/Postman):
   - confirmar resposta HTTP
5. Checar logs do sistema de origem:
   - tentativas de envio
   - códigos de resposta
6. Checar logs do sistema de destino:
   - recebimento do evento
   - erros de processamento
7. Se a integração parou de funcionar:
   - verificar mudanças recentes (deploy, alteração de schema)
   - validar se houve bloqueio por rate limit
8. Persistindo o problema:
   - coletar evidências mínimas
   - escalar para análise técnica

## Perguntas de diagnóstico
- Qual é o endpoint configurado?
- Qual evento deveria ser enviado?
- O erro ocorre em todas as tentativas ou apenas algumas?
- Há
