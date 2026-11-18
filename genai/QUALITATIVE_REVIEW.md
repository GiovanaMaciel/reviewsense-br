# Revisão qualitativa exploratória

## Escopo

Inspeção do relatório de uma execução em 12 avaliações sintéticas. Esta revisão
não constitui anotação humana independente, benchmark de fidelidade ou avaliação
de generalização. O relatório bruto e os metadados foram preservados. Nenhuma
conclusão foi reescrita silenciosamente no resultado original.

## Integridade das referências

- 14 citações verificadas: IDs existentes e trechos literais correspondentes.
- As quatro sugestões referenciam avaliações citadas nas reclamações.
- Esses controles não comprovam sustentação semântica de todas as descrições.

## Observações por conclusão

| Grupo | Avaliação exploratória | Observação | Redação proposta |
|---|---|---|---|
| Entrega pontual e comida deliciosa | supported_with_scope_caution | Pontualidade é apoiada por R03 e R12; sabor é elogiado apenas em R03 dentro das evidências deste grupo. | R03 elogia o horário e o sabor; R12 relata chegada antes do prazo e pedido completo. |
| Embalagem bem feita e organização | partially_supported | Fechamento e organização estão nos textos. A palavra segura pode sugerir uma avaliação de segurança não realizada. | R01 menciona embalagem bem fechada e R06 destaca organização. |
| Sabor e porção elogiados | partially_supported | Sabor e porção estão em R08, mas a redação pelos clientes generaliza uma única avaliação citada. | A avaliação R08 elogia o sabor e a porção. |
| Atendimento ágil e solução de problemas | supported | R11 sustenta resposta rápida e resolução da troca. | R11 relata atendimento rápido e resolução da troca do item. |
| Comida chegando fria | supported_with_scope_caution | As três avaliações mencionam comida fria. O impacto na experiência é uma inferência, não uma medição adicional. | R01, R02 e R09 relatam comida ou lanche frio. |
| Atraso na entrega | supported_with_scope_caution | Atrasos são explícitos. Insatisfação é uma interpretação do teor das reclamações. | R02 relata atraso e R07 menciona espera além do prazo informado. |
| Itens faltantes no pedido | supported_with_scope_caution | Bebida ausente aparece em R04 e R05; atendimento sem solução aparece apenas em R05. | R04 e R05 relatam bebida ausente; R05 também menciona atendimento sem solução. |
| Problemas com a embalagem | partially_supported | Há apenas R10. Algumas entregas amplia a frequência; abriu não demonstra necessariamente ruptura do material. | R10 relata que a embalagem abriu durante a entrega e houve vazamento de molho. |

As redações propostas são sugestões editoriais desta inspeção, não novas saídas
do modelo nem resultados usados para calcular uma taxa de acerto.

## Sugestões de ação

1. **Temperatura:** há reclamações correspondentes, mas a medida operacional deve
   ser testada; a causa da comida fria não foi identificada pelas avaliações.
2. **Rotas e logística:** investigar é pertinente, mas não há evidência de que
   a rota tenha causado o atraso. A proposta não equivale a um diagnóstico.
3. **Checklist:** pode ser investigado para conferência dos pedidos. As evidências
   citam bebidas, e não comprovam ausência de outros complementos.
4. **Embalagens:** R10 relata abertura e vazamento. Resistência do material é uma
   hipótese entre outras; vedação e manuseio também precisam ser investigados.

## Cobertura e protocolo

Os quatro assuntos negativos de referência do lote aparecem no relatório.
Isso não mede cobertura em avaliações reais nem garante citações exaustivas
de todo assunto positivo. Não foi calculado um escore agregado de fidelidade.

A tentativa anterior com GPT-OSS 20B e prompt v1 falhou por objetos serializados
como strings no JSON. A execução registrada utilizou GPT-OSS 120B e prompt v2.
Como modelo e prompt mudaram juntos, essas observações não isolam o efeito de
cada alteração nem constituem comparação controlada entre modelos.

## Próxima avaliação

Revisão humana independente e lotes separados com exemplos positivos,
negativos, mistos, informações insuficientes e instruções adversariais.
Fidelidade, cobertura, utilidade e robustez devem ter critérios explícitos.
