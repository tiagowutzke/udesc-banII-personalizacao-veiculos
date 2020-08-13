SELECT
		v.placa,
		mc.descricao || ' ' || m.descricao
	FROM
		veiculos v
	JOIN
		modelo m
		USING(cod_modelo)
	JOIN
		marcas mc
		USING(cod_marca)
	WHERE
		cpf_cliente = '%value%'