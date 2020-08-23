SELECT
	p.cod_personalizacao,
	c.cpf,
	c.nome,
	v.placa,
	m.descricao ||' '|| md.descricao,
	to_char(DATA, 'dd/mm/YYYY'),
	data,
	valor_total,
  (select count(*) from contas_receber where cod_personalizacao = p.cod_personalizacao)
FROM
	personalizacoes p
JOIN
	veiculos v
	ON v.placa = p.placa_veiculo
JOIN
	modelo md
	USING(cod_modelo)
JOIN
	marcas m
	USING(cod_marca)
JOIN
	clientes c
	ON c.cpf = v.cpf_cliente