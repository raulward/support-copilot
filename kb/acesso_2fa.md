# 2FA não chega ou falha na autenticação

## Quando usar
- Quando o usuário relata que o código de verificação (2FA) não chega.
- Quando o usuário recebe erro ao validar o código (código inválido/expirado).
- Quando o usuário troca de celular e perde acesso ao método de 2FA.

## Sintomas comuns
- “Não recebo o código por SMS/e-mail/app.”
- “O código chega, mas dá inválido.”
- “Meu celular trocou e perdi o autenticador.”
- “Minha conta ficou bloqueada após várias tentativas.”

## Procedimento
1. Confirmar o método de 2FA configurado (SMS, e-mail, aplicativo autenticador).
2. Validar se o usuário está usando o mesmo e-mail/telefone cadastrado.
3. Pedir para o usuário checar:
   - pasta de spam (se for e-mail)
   - bloqueio de SMS / modo avião (se for SMS)
   - horário automático do aparelho (se for app autenticador)
4. Se for SMS:
   - confirmar DDD e número completo
   - orientar tentar novamente após 2–3 minutos
5. Se for e-mail:
   - orientar adicionar o remetente à lista segura
   - tentar reenviar e checar spam/lixo eletrônico
6. Se for app autenticador:
   - confirmar se o relógio do celular está em “ajuste automático”
   - orientar remover e reconfigurar o autenticador (se aplicável)
7. Se houver bloqueio por tentativas:
   - informar tempo de bloqueio (ex.: 15 minutos) e orientar aguardar
8. Persistindo o problema:
   - coletar evidências mínimas (horário aproximado, método, prints, e-mail/ID)
   - seguir para escalonamento

## Perguntas de diagnóstico
- Qual método de 2FA você usa (SMS, e-mail ou app autenticador)?
- Qual é o e-mail/telefone cadastrado na conta?
- Desde quando o problema ocorre? Acontece em todas as tentativas?
- Você trocou de celular/operadora recentemente?
- Você consegue receber outros SMS/e-mails normalmente?
- Pode enviar um print do erro (se houver)?

## Escalonamento
- Quando escalar:
  - Falha persistente após seguir o procedimento
  - Vários usuários afetados simultaneamente
  - Indícios de instabilidade do serviço de autenticação
- Para quem escalar:
  - Time técnico responsável por autenticação/infra
- Evidências mínimas:
  - ID/e-mail do usuário
  - método de 2FA
  - horário aproximado das tentativas
  - prints/erros exibidos
  - região/operadora (se SMS)
