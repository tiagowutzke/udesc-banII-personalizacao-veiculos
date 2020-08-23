SELECT
	cod_mecanico,
	nome
FROM
	mecanicos
WHERE
	cod_especialidade = %value%
