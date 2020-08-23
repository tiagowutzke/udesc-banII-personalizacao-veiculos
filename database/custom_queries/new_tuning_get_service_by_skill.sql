SELECT
	cod_servico,
	valor,
	descricao
FROM
	servicos
WHERE
	cod_especialidade = %value%