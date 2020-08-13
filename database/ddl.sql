-- DROP DATABASE personalizacao_veiculos
CREATE DATABASE personalizacao_veiculos

--DROP TABLE public.especialidade;
CREATE TABLE public.especialidade (
	cod_especialidade serial NOT NULL,
	nome varchar(255) NOT NULL,
	CONSTRAINT especialidade_pk PRIMARY KEY (cod_especialidade)
);

--DROP TABLE public.servicos;
CREATE TABLE public.servicos (
	cod_servico serial NOT NULL,
	descricao varchar(255) NOT NULL,
	valor numeric(2) NOT NULL,
	cod_especialidade int4 NOT NULL,
	CONSTRAINT servicos_pk PRIMARY KEY (cod_servico),
	CONSTRAINT servicos_fk FOREIGN KEY (cod_especialidade) REFERENCES public.especialidade(cod_especialidade)
);

--DROP TABLE public.mecanicos;
CREATE TABLE public.mecanicos (
	cod_mecanico serial NOT NULL,
	nome varchar(255) NOT NULL,
	cod_especialidade int4 NOT NULL,
	CONSTRAINT mecanicos_pk PRIMARY KEY (cod_mecanico),
	CONSTRAINT mecanicos_fk FOREIGN KEY (cod_especialidade) REFERENCES public.especialidade(cod_especialidade)
);

--DROP TABLE public.marcas;
CREATE TABLE public.marcas (
	cod_marca serial NOT NULL,
	descricao varchar(255) NOT NULL,
	CONSTRAINT marcas_pk PRIMARY KEY (cod_marca)
);

--DROP TABLE public.modelo;
CREATE TABLE public.modelo (
	cod_modelo serial NOT NULL,
	descricao varchar(255) NOT NULL,
	tipo varchar(150) NULL,
	motor numeric(1) NULL,
	ano_modelo int4 NOT NULL,
	e_importado boolean NOT NULL DEFAULT FALSE,
	cod_marca int4 NOT NULL,
	CONSTRAINT modelo_pk PRIMARY KEY (cod_modelo),
	CONSTRAINT modelo_fk FOREIGN KEY (cod_marca) REFERENCES public.marcas(cod_marca)
);

--DROP TABLE public.pecas;
CREATE TABLE public.pecas (
	cod_peca serial NOT NULL,
	descricao varchar(255) NOT NULL,
	valor numeric(2) NOT NULL,
	quantidade int4 NOT NULL,
	categoria varchar(150) NULL,
	e_original bool NOT NULL DEFAULT FALSE,
	cod_modelo int4 NOT NULL,
	CONSTRAINT pecas_pk PRIMARY KEY (cod_peca),
	CONSTRAINT pecas_fk FOREIGN KEY (cod_modelo) REFERENCES public.modelo(cod_modelo)
);

--DROP TABLE public.clientes;
CREATE TABLE public.clientes (
	cpf varchar(11) NOT NULL,
	telefone varchar(11) NULL,
	logradouro varchar(255) NULL,
	bairro varchar(255) NULL,
	cep varchar(8) NULL,
	CONSTRAINT clientes_pk PRIMARY KEY (cpf)
);

--DROP TABLE public.contas_receber;
CREATE TABLE public.contas_receber (
	cod_recebimento serial NOT NULL,
	data_vencimento date NOT NULL,
	valor_parcela numeric(2) NOT NULL,
	num_parcela int4 NOT NULL,
	total_parcelas int4 NOT NULL,
	parcela_paga bool NOT NULL DEFAULT FALSE,
	cpf_cliente varchar(11) NOT NULL,
	CONSTRAINT contas_receber_pk PRIMARY KEY (cod_recebimento),
	CONSTRAINT contas_receber_fk FOREIGN KEY (cpf_cliente) REFERENCES public.clientes(cpf)
);

--DROP TABLE public.veiculos;
CREATE TABLE public.veiculos (
	chassi varchar(30) NOT NULL,
	placa varchar(7) NOT NULL,
	ano_fabricacao int4 NOT NULL,
	cor varchar(20) NOT NULL,
	combustivel varchar(20) NOT NULL,
	kilometragem int8 NOT NULL,
	cpf_cliente varchar(11) NOT NULL,
	cod_modelo int4 NOT NULL,
	CONSTRAINT veiculos_pk PRIMARY KEY (chassi,placa),
	CONSTRAINT veiculos_fk FOREIGN KEY (cpf_cliente) REFERENCES public.clientes(cpf),
	CONSTRAINT veiculos_fk_1 FOREIGN KEY (cod_modelo) REFERENCES public.modelo(cod_modelo)
);

--DROP TABLE public.personalizacoes;
CREATE TABLE public.personalizacoes (
	cod_personalizacao serial NOT NULL,
	data date NOT NULL,
	valor_total numeric(2) NOT NULL,
	cod_recebimento int4 NOT NULL,
	cod_mecanico int4 NOT NULL,
	chassi_veiculo varchar(30) NOT NULL,
	placa_veiculo varchar(7) NOT NULL,
	cod_peca int4 NOT NULL,
	cod_servico int4 NOT NULL,
	CONSTRAINT personalizacoes_pk PRIMARY KEY (cod_personalizacao),
	CONSTRAINT personalizacoes_contas_receber_fk FOREIGN KEY (cod_recebimento) REFERENCES public.contas_receber(cod_recebimento),
	CONSTRAINT personalizacoes_mecanico_fk FOREIGN KEY (cod_mecanico) REFERENCES public.mecanicos(cod_mecanico),
	CONSTRAINT personalizacoes_veiculos_fk FOREIGN KEY (chassi_veiculo, placa_veiculo) REFERENCES public.veiculos(chassi, placa),
	CONSTRAINT personalizacoes_pecas_fk FOREIGN KEY (cod_peca) REFERENCES public.pecas(cod_peca),
	CONSTRAINT personalizacoes_servicos_fk FOREIGN KEY (cod_servico) REFERENCES public.servicos(cod_servico)
);






