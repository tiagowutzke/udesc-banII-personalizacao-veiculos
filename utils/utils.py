def get_table_template(table):
    templates = {
        'clientes': 'customers_table_body.html',
        'mecanicos': 'mechanics_table_body.html',
        'pecas': 'auto_parts_table_body.html',
        'veiculos': 'vehicles_customers_table_body.html',
        'especialidade': 'combo_box_template.html',
        'marcas': 'combo_box_template.html',
        'tunnings-by-customer': 'combo_box_template.html',
        # New tunning page
        'new-tuning-vehicle': 'combo_box_template.html',
        'new-tuning-mechanics': 'combo_box_template.html',
        'new-tuning-services': 'combo_box_multi_template.html',
        'new-tuning-parts': 'combo_box_multi_template.html',
    }
    return templates[table]


def router_page(page):
    router_functions = {
        'clientes': 'customers_page',
        'mecanicos': 'mechanics_page',
        'servicos': 'services_page',
        'modelo': 'models_page',
        'pecas': 'auto_parts_page',
        'veiculos': 'vehicles_customers_page',
        'especialidade': 'success',
        'marcas': 'success',
        'personalizacoes': 'success',
        'personalizacoes_servicos': 'success',
        'personalizacoes_pecas': 'success',
        'contas_receber': 'receivables_page'
    }
    return router_functions[page]
