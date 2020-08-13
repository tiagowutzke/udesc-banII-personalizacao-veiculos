SELECT
    cod_peca,
    p.descricao,
    valor,
    quantidade,
    categoria,
    e_original,
    m.cod_modelo,
    m.descricao,
    mc.descricao
FROM
	pecas p
JOIN
	modelo m
	USING(cod_modelo)
JOIN
	marcas mc
	USING(cod_marca)