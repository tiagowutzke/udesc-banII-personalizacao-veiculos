SELECT
	cod_personalizacao,
	p.descricao,
	p.valor,
	p.cod_peca
FROM
	personalizacoes_pecas pp
JOIN
	pecas p
	USING(cod_peca)
WHERE
	cod_personalizacao = %value%