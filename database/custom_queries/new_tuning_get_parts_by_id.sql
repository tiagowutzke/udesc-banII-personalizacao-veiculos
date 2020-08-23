SELECT
	cod_peca,
	valor,
	p.descricao || ' (' || mc.descricao || ' ' || m.descricao || ')'
FROM
	pecas p
JOIN
	modelo m
	USING(cod_modelo)
JOIN
	marcas mc
	USING(cod_marca)
WHERE
	cod_peca = %value%