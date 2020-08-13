-- Verifica se já existe um contas a receber cadastrado para uma personalização.
-- Se já existe, não permite a inserção, pois o correto seria inserir uma nova parcela no
-- contas a receber já existente
CREATE OR REPLACE FUNCTION receivable_check() RETURNS TRIGGER AS
$$
BEGIN
	IF (SELECT count(cod_recebimento) FROM contas_receber WHERE cod_personalizacao = NEW.cod_personalizacao) > 0
		AND (SELECT DISTINCT cod_recebimento FROM contas_receber WHERE cod_personalizacao = NEW.cod_personalizacao) <> NEW.cod_recebimento
	THEN
		RAISE EXCEPTION 'Já existe um contas a receber para esta personalização! Insira uma nova parcela no contas a receber já cadastrado!';
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER receivable_check BEFORE INSERT ON contas_receber
FOR EACH ROW EXECUTE PROCEDURE receivable_check()

-- Quando houver inserção de novas parcelas em um contas a receber
-- atualiza o valor de total de parcelas
CREATE OR REPLACE FUNCTION update_quota() RETURNS TRIGGER AS
$$
BEGIN
	UPDATE contas_receber
	SET total_parcelas = NEW.total_parcelas
	WHERE cod_recebimento = NEW.cod_recebimento;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_quota BEFORE INSERT ON contas_receber
FOR EACH ROW EXECUTE PROCEDURE update_quota()


-- Não permitir inserção de novas personalizações se o cliente
-- tiver mais de 5000 reais em parcelas atrasadas
CREATE OR REPLACE FUNCTION check_overdue() RETURNS TRIGGER AS
$$
BEGIN
	IF (
		SELECT sum(valor_parcela)
		FROM contas_receber c
		JOIN veiculos v ON v.cpf_cliente = c.cpf_cliente
		WHERE v.chassi = NEW.chassi_veiculo
		AND NOT parcela_paga
	) > 5000 THEN
		RAISE EXCEPTION 'Cliente inadimplente, não foi possível inserir nova personalização!';
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER check_overdue BEFORE INSERT ON personalizacoes
FOR EACH ROW EXECUTE PROCEDURE check_overdue()


-- Impedir a inserção de veículo com placa incorreta (padrão novo e antigo)
CREATE OR REPLACE FUNCTION is_valid_license_plate(plate text)
 RETURNS bool
 LANGUAGE plpgsql
AS $function$
DECLARE plate_check bool;
BEGIN
	SELECT plate ~ '[A-Z]{3}[0-9]{4}' OR plate ~ '[A-Z]{3}[0-9][A-Z][0-9]{2}' INTO plate_check;
	RETURN plate_check;
END
$function$
;

CREATE OR REPLACE FUNCTION license_plate_check() RETURNS TRIGGER AS
$$
BEGIN
	IF (NOT is_valid_license_plate(NEW.placa)) THEN
		RAISE EXCEPTION 'Placa inválida!';
	END IF;
	RETURN NEW;
END
$$
LANGUAGE plpgsql;

CREATE TRIGGER license_plate_check BEFORE INSERT OR UPDATE ON veiculos
FOR EACH ROW EXECUTE PROCEDURE license_plate_check();