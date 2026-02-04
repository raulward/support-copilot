# Incidentes: primeiros passos e triagem inicial

## Quando usar
- Quando o sistema apresenta instabilidade ou indisponibilidade.
- Quando múltiplos usuários relatam erro ao mesmo tempo.
- Quando há aumento significativo de latência ou falhas.
- Quando um serviço crítico está fora do ar.

## Sintomas comuns
- “O sistema está fora do ar.”
- “Está muito lento.”
- “Recebo erro 500/502.”
- “Funcionava antes e parou de repente.”
- “Vários usuários reclamando do mesmo problema.”

## Procedimento
1. Confirmar o impacto:
   - quantos usuários afetados
   - quais funcionalidades estão indisponíveis
2. Confirmar o horário aproximado do início do incidente.
3. Verificar se o problema é:
   - total (serviço fora do ar)
   - parcial (apenas algumas funções)
4. Checar se houve mudanças recentes:
   - deploy
   - configuração
   - integração externa
5. Orientar ações imediatas:
   - tentar reproduzir o erro
   - coletar mensagens/códigos de erro
6. Se houver workaround conhecido:
   - informar o usuário claramente
7. Registrar o incidente:
   - abrir ticket interno de incidente
   - documentar status e próximos passos

## Perguntas de diagnóstico
- Desde quando o problema ocorre?
- O problema acontece para todos os usuários?
- Qual erro ou mensagem aparece?
- Alguma ação foi realizada antes do problema (deploy, configuração)?
- O problema ocorre em todos os canais (web, mobile, API)?

## Escalonamento
- Quando escalar:
  - Impacto alto ou crítico (P0/P1)
  - Afeta múltiplos clientes
  - Serviço essencial indisponível
- Para quem escalar:
  - Time técnico responsável pela infraestrutura/serviço
- Evidências mínimas:
  - horário do início
  - mensagens/códigos de erro
  - serviços afetados
  - prints/logs disponíveis
