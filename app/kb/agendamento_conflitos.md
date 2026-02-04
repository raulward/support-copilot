# Agendamento: conflito de horários, reagendamento e confirmações

## Quando usar
- Quando o usuário relata conflito de agenda (horário já ocupado).
- Quando o agendamento não confirma ou não envia notificação.
- Quando há necessidade de reagendar sem perder o histórico.
- Quando há dúvidas sobre fuso horário.

## Sintomas comuns
- “O sistema não deixa agendar porque o horário está ocupado.”
- “Agendei, mas não recebi confirmação.”
- “O cliente marcou, mas não apareceu no calendário.”
- “O horário ficou errado (fuso).”
- “Preciso reagendar sem cancelar.”

## Procedimento
1. Confirmar o fuso horário do usuário e do sistema:
   - orientar manter fuso e horário do dispositivo em automático
2. Validar regras de disponibilidade:
   - janelas de atendimento
   - duração padrão do evento
   - tempo mínimo de antecedência (ex.: 30 min/1h)
3. Em caso de conflito:
   - sugerir 3 horários alternativos próximos (antes/depois)
   - verificar se existem buffers entre reuniões (ex.: 10–15 min)
4. Em caso de falta de confirmação/notificação:
   - checar se o e-mail/telefone do destinatário está correto
   - orientar checar spam (se e-mail)
   - checar bloqueios de notificações no dispositivo
5. Em reagendamento:
   - registrar motivo do reagendamento
   - manter histórico do agendamento anterior (para rastreabilidade)
6. Se houver integração com calendário (Google/Outlook):
   - confirmar permissão e sincronização
   - checar se houve revogação de acesso
7. Persistindo o problema:
   - coletar evidências mínimas e escalar

## Perguntas de diagnóstico
- Qual horário você tentou agendar (data e hora)?
- Qual é o seu fuso horário e o do cliente?
- O conflito acontece para todos os horários ou apenas alguns?
- Você está usando integração com calendário? Qual (Google/Outlook)?
- Houve mudança recente de permissões ou conta conectada?
- O problema ocorre em web, celular ou ambos?

## Escalonamento
- Quando escalar:
  - Conflitos incoerentes (agenda livre mas sistema acusa ocupado)
  - Notificações falhando para muitos usuários
  - Integração de calendário com erro recorrente
- Para quem escalar:
  - Time técnico responsável por integrações/agenda
- Evidências mínimas:
  - ID do evento (se existir)
  - data/hora e fuso
  - e-mails envolvidos
  - prints do erro
  - informação da integração (Google/Outlook) e status de permissão
