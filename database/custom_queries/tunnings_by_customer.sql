SELECT DISTINCT
	p.cod_personalizacao,
	mc.descricao  ||' '|| m.descricao ||
	'  R$ ' || p.valor_total || '  ' ||
	to_char(p."data", 'dd/mm/YYYY')
FROM
	personalizacoes p
JOIN
	veiculos v
	ON p.placa_veiculo = v.placa
JOIN
	modelo m
	USING(cod_modelo)
JOIN
	marcas mc
	USING(cod_marca)
WHERE
	v.cpf_cliente = %value%::text