SELECT
	cod_personalizacao,
	s.descricao,
	s.valor,
	m.nome,
	s.cod_servico,
	m.cod_mecanico
FROM
	personalizacoes_servicos ps
JOIN
	servicos s
	USING(cod_servico)
JOIN
	mecanicos m
	USING(cod_mecanico)
WHERE
	cod_personalizacao = %value%