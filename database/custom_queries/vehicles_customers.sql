SELECT
	chassi,
	placa,
	ano_fabricacao,
	cor,
	combustivel,
	kilometragem,
	c.nome,
	mc.descricao || ' ' || m.descricao,
  m.cod_modelo,
  c.cpf
FROM
	veiculos v
LEFT JOIN
	clientes c
	ON v.cpf_cliente = c.cpf
LEFT JOIN
	modelo m
	USING(cod_modelo)
LEFT JOIN
	marcas mc
	ON mc.cod_marca = m.cod_marca