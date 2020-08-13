import os
from flask import Flask, render_template, request, redirect, url_for

from database.database_adapter import DatabaseAdapter
from utils.utils import get_table_template, router_page

app = Flask(__name__)

from environ import set_environ_variables
set_environ_variables()

# pages
index_route = "/"
customers_route = "/customers"
mechanics_route = "/mechanics"
services_route = "/services"
vehicles_models = "/modelos"
vehicles_customers = '/veiculos'
auto_parts = "/pecas"
new_tuning = '/nova-personalizacao'
tunnings = '/personalizacoes'
receivables = '/contas-receber'

# data manipulation endpoints
update_row = "/update"
insert_row = "/insert"
insert_receivable = "/insert_receivable"
delete_row = "/delete"
query_combo_values = "/query_combo_values"
success_route = "/success"

# new tuning backend
get_combo_values = '/get_combo_values'


# PAGES TEMPLATES
@app.route(index_route)
def index():
    return render_template('index.html', title='PERSONALIZAÇÃO DE VEÍCULOS')


@app.route(customers_route)
def customers_page():
    database = DatabaseAdapter()
    customers = database.select_all('clientes', '*')
    database.close()
    return render_template('customers.html', title='Clientes', rows=customers)


@app.route(mechanics_route)
def mechanics_page():
    database = DatabaseAdapter()

    combo_values = database.select_all('especialidade', '*')
    new_value = 'Inserir especialidade'

    mechanics = database.select_all_joined(
        from_table='mecanicos m',
        join_table='especialidade e',
        on='cod_especialidade',
        how='left',
        columns=['cod_mecanico', 'm.nome', 'e.nome', 'm.cod_especialidade']
    )

    database.close()
    return render_template(
        'mechanics.html',
        title='Mecânicos',
        rows=mechanics,
        combo_box=combo_values,
        new_value=new_value
    )


@app.route(services_route)
def services_page():
    database = DatabaseAdapter()

    combo_values = database.select_all('especialidade', '*')
    new_value = 'Inserir especialidade'

    services = database.select_all_joined(
        from_table='servicos s',
        join_table='especialidade e',
        on='cod_especialidade',
        how='left',
        columns=['cod_servico', 's.descricao', 'valor', 'e.nome', 's.cod_especialidade']
    )

    database.close()
    return render_template(
        'services.html',
        title='Serviços',
        rows=services,
        combo_box=combo_values,
        new_value=new_value
    )


@app.route(vehicles_models)
def models_page():
    database = DatabaseAdapter()

    combo_values = database.select_all('marcas', '*')
    new_value_label = 'Inserir marca'

    vehicles_models = database.select_all_joined(
        from_table='modelo md',
        join_table='marcas mc',
        on='cod_marca',
        how='left',
        columns=[
            'cod_modelo',
            'md.descricao',
            'tipo',
            'motor',
            'ano_modelo',
            'e_importado',
            'mc.cod_marca',
            'mc.descricao'
        ]
    )

    database.close()
    return render_template(
        'vehicles_models.html',
        title='Modelos',
        rows=vehicles_models,
        combo_box=combo_values,
        new_value=new_value_label
    )


@app.route(auto_parts)
def auto_parts_page():
    database = DatabaseAdapter()

    combo_values = database.select_all_joined (
        from_table='modelo md',
        join_table='marcas mc',
        on='cod_marca',
        columns=[
            'cod_modelo',
            "mc.descricao || ' ' || md.descricao"
        ]
    )
    new_value_label = 'Inserir modelo'

    auto_parts = database.select_custom_sql("auto_parts")

    database.close()
    return render_template(
        'auto_parts.html',
        title='Auto peças',
        rows=auto_parts,
        combo_box=combo_values,
        new_value=new_value_label
    )


@app.route(vehicles_customers)
def vehicles_customers_page():
    database = DatabaseAdapter()

    # Combo box1
    vehicles_models = database.select_all_joined(
        from_table='modelo md',
        join_table='marcas mc',
        on='cod_marca',
        columns=[
            'cod_modelo',
            "mc.descricao || ' ' || md.descricao"
        ]
    )
    # Combo box2
    customers = database.select_all('clientes', 'cpf', 'nome')

    vehicles = database.select_custom_sql("vehicles_customers")

    database.close()
    return render_template(
        'vehicles_customers.html',
        title='Veículos proprietários',
        rows=vehicles,
        combo_box1=vehicles_models,
        combo_box2=customers
    )


@app.route(new_tuning)
def new_tuning_page():
    title = 'Nova personalização'
    default = None

    database = DatabaseAdapter()

    edit_id = request.args.get('tunning_id')

    if edit_id:
        title = 'Editar personalização'
        default = {
            'tunning_id': edit_id,
            'customer': request.args.get('customer'),
            'vehicle': request.args.get('vehicle'),
            'date': request.args.get('date'),
            'quotas': request.args.get('quotas'),
            'value': request.args.get('value'),
            'services_details': database.select_custom_sql(
                'tunnings_service_details',
                where_value=str(edit_id)
            ),
            'parts_details':  database.select_custom_sql(
                'tunnings_part_details',
                where_value=str(edit_id)
            )
        }

    # Combo box
    customers = database.select_all('clientes', 'cpf', 'nome')
    skills = database.select_all('especialidade', '*')
    auto_parts = database.select_all('pecas', 'cod_peca', 'valor', 'descricao')

    database.close()
    return render_template(
        'new_tuning.html',
        title=title,
        combo_box_customers=customers,
        combo_box_skills=skills,
        combo_box_parts=auto_parts,
        default=default
    )


@app.route(tunnings)
def tunning_page():
    database = DatabaseAdapter()
    tunnings = database.select_custom_sql('tunnings')

    services_details = [
        database.select_custom_sql(
            'tunnings_service_details',
            where_value=str(tunning_id[0])
        )
        for tunning_id in tunnings
    ]

    parts_details = [
        database.select_custom_sql(
            'tunnings_part_details',
            where_value=str(tunning_id[0])
        )
        for tunning_id in tunnings
    ]

    database.close()
    return render_template(
        'tunnings.html',
        title='Personalizações',
        rows=tunnings,
        services_details=services_details,
        parts_details=parts_details
    )


@app.route(receivables)
def receivables_page():
    database = DatabaseAdapter()

    receivables = database.select_all_joined(
        from_table='contas_receber',
        join_table='clientes',
        on=['cpf_cliente', 'cpf'],
        columns=[
            "cod_recebimento",
            "nome",
            "num_parcela",
            "total_parcelas",
            "valor_parcela",
            "data_vencimento",
            "to_char(data_vencimento, 'dd/mm/YYYY')",
            "parcela_paga"
        ]
    )
    # Combo box
    customers = database.select_all_joined(
        from_table='clientes',
        join_table='contas_receber',
        on=['cpf', 'cpf_cliente'],
        columns=['cpf', 'nome']
    )

    database.close()
    return render_template(
        'receivables.html',
        title='Contas a receber',
        rows=receivables,
        combo_box=customers
    )


# DML BACKEND
@app.route(update_row)
def update_row_function():
    dml = {
        'table': request.args.get('table'),
        'column': request.args.get('column'),
        'old_id': request.args.get('old_id'),
        'cast': request.args.get('cast')
    }

    sql_cast = dml['cast'] or 'text'

    cols_values = {
        key: value
        for key, value in request.args.items()
        if key not in dml.keys()
    }

    database = DatabaseAdapter()
    update_result = database.persistence.update_by_col(
        table=dml['table'],
        where_col=dml['column'],
        where_value=dml['old_id'],
        cols_values=cols_values,
        cast_to=sql_cast
    )

    if not update_result['success']:
        database.close()
        return {
            'status': 'error',
            'message': update_result['message']
        }

    database.close()
    return redirect(
        url_for(router_page(dml['table']))
    )


@app.route(insert_row)
def insert_row_function():
    dml = {
        'table': request.args.get('table'),
        'no_quotes': request.args.get('no_quotes'),
    }

    cols_values = {
        key: value
        for key, value in request.args.items()
        if key not in dml.keys()
    }

    database = DatabaseAdapter()
    insert_result = database.persistence.insert_row(
        table=dml['table'],
        cols_values=cols_values,
        no_string_quotes=dml['no_quotes']
    )

    if not insert_result['success']:
        database.close()
        return {
            'status': 'error',
            'message': insert_result['message']
        }

    database.close()
    return redirect(
        url_for(router_page(dml['table']))
    )


@app.route(insert_receivable)
def insert_receivable_function():
    cols_values = {
        key: value
        for key, value in request.args.items()
    }

    cols_values['cod_recebimento'] = f"""(
        select distinct cod_recebimento 
        from contas_receber
        where cod_personalizacao = {cols_values['cod_personalizacao']}
    )"""

    cols_values['num_parcela'] = f"""(
        select max(num_parcela)+1 
        from contas_receber
        where cod_personalizacao = {cols_values['cod_personalizacao']}
    )"""

    database = DatabaseAdapter()
    insert_result = database.persistence.insert_row(
        table='contas_receber',
        cols_values=cols_values,
        no_string_quotes=[cols_values['cod_recebimento'], cols_values['num_parcela']]
    )

    if not insert_result['success']:
        database.close()
        return {
            'status': 'error',
            'message': insert_result['message']
        }

    database.close()
    return redirect(
        url_for(router_page('contas_receber'))
    )


@app.route(delete_row)
def delete_row_function():
    table = request.args.get('table')
    id = request.args.get('id')
    column = request.args.get('column')

    database = DatabaseAdapter()
    delete_result = database.persistence.delete_by_col(
        table=table,
        where_col=column,
        where_value=id
    )

    if not delete_result['success']:
        database.close()
        return {
            'status': 'error',
            'message': delete_result['message']
        }

    database.close()
    return redirect(
        url_for(router_page(table))
    )


@app.route(query_combo_values)
def query_combo_function():
    table = request.args.get('table')
    column = request.args.get('column')
    pkey = request.args.get('pkey')

    database = DatabaseAdapter()
    combo_values = database.select_all(table, pkey, column)

    database.close()
    template = get_table_template(table)
    new_value_label = f'Inserir {table}'
    return render_template(template, combo_box=combo_values, new_value=new_value_label)


# New tuning back end
@app.route(get_combo_values)
def get_combo_values_function():
    database = DatabaseAdapter()

    value = request.args.get('value')
    entity = request.args.get('entity')

    sql_templates = {
        'new-tuning-vehicle': 'new_tuning_get_customer_vehicles',
        'new-tuning-services': 'new_tuning_get_service_by_skill',
        'new-tuning-mechanics': 'new_tuning_get_mechanics_by_skill',
        'new-tuning-parts': 'new_tuning_get_parts_by_id',
        'tunnings-by-customer': 'tunnings_by_customer'
    }

    combo_values = database.select_custom_sql(
        sql_templates[entity],
        where_value=value
    )

    template = get_table_template(entity)
    return render_template(template, combo_box=combo_values)


@app.route(success_route)
def success():
    return {'status': 'success'}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
