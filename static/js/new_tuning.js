    function get_combo_values(combo_box, entity, combo_to_change){
       selected_value = $('#'+combo_box.id).children('option:selected').val();

       $.ajax({
          url: "/get_combo_values",
          type: "get",
          data: {
            value: selected_value,
            entity: entity
          },
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao buscar os registros:\n' + response.message);
            else $(combo_to_change).html(response);
          },
          error: function(response) {
            window.alert('Erro ao buscar os registros:\n' + response);
          }
       });
    }

    function set_hidden_value(combo_box, input_id){
       selected_value = $('#'+combo_box.id).children('option:selected').val();
       $(input_id).val(selected_value);

       should_enable_submit();
    }

    row_index=0
    function add_service(){
        row_index++
        // Service
        service_selected = $('#services').children("option:selected")
        service_id = service_selected.attr("id");
        service_value = service_selected.val();
        service_description = service_selected.text();
        // Mechanic
        mechanic_selected = $('#mechanics').children("option:selected");
        mechanic_id = mechanic_selected.val();
        mechanic_description = mechanic_selected.text();
        // Table row
        new_row = `
            <tr id="${row_index}">
                <td class="column1 service" id="${service_id}">${service_description}</td>
                <td class="column3 mechanic" id="${mechanic_id}">${mechanic_description}</td>
                <td class="column3 value">${service_value}</td>
                <td class="column3">
                    <button style="border-width: 2px;font-size: 1em;height: 2em;padding: 0.3em;" onclick="remove_service(${row_index})" class="btn btn-outline-danger">Remover</button>
                </td>
            </tr>
        `
        // Adding new row
        $('#tbody').append(new_row);
        // Adding total value
        total_value = parseFloat($('#tunning-value').text()) + parseFloat(service_value)
        $('#tunning-value').text(total_value);

        should_enable_submit();
    }

    function remove_service(row_index){
        // Updating total value
        service_value = $('tr#'+row_index+' td.value').text();
        total_value = parseFloat($('#tunning-value').text()) - parseFloat(service_value);
        $('#tunning-value').text(total_value);
        // Removing element
        $('#tbody tr#'+row_index).remove();
    }

    function add_parts(){
        row_index++
        // Parts
        part_selected = $('#parts').children("option:selected")
        part_id = part_selected.attr("id");
        part_value = part_selected.val();
        part_description = part_selected.text();
        // Table row
        new_row = `
            <tr id="${row_index}">
                <td class="column1 part" id="${part_id}">${part_description}</td>
                <td class="column3 value">${part_value}</td>
                <td class="column3">
                    <button style="border-width: 2px;font-size: 1em;height: 2em;padding: 0.3em;" onclick="remove_part(${row_index})" class="btn btn-outline-danger">Remover</button>
                </td>
            </tr>
        `
        // Adding new row
        $('#tbody2').append(new_row);
        // Adding total value
        total_value = parseFloat($('#tunning-value').text()) + parseFloat(part_value)
        $('#tunning-value').text(total_value);

        should_enable_submit();
    }

    function remove_part(row_index){
        // Updating total value
        part_value = $('tr#'+row_index+' td.value').text();
        total_value = parseFloat($('#tunning-value').text()) - parseFloat(part_value);
        $('#tunning-value').text(total_value);
        // Removing element
        $('#tbody2 tr#'+row_index).remove();
    }

    function should_enable_submit(){
        has_customer = $('#customer').val();
        has_vehicle = $('#vehicle').val();
        has_total_value = parseFloat($('#tunning-value').text()) > 0;

        if(has_customer && has_vehicle && has_total_value)
            $('#submit-tunning').prop('disabled', false);
    }

    function submit_new_tunning(){
       if (!confirm("Confirma a gravação da personalização?")) return false;

       // Tunning
       var payload = {
            'table': 'personalizacoes',
            'data': $(':input[type="date"]').val(),
            'valor_total': $('#tunning-value').text(),
            'placa_veiculo': $('#vehicle').children('option:selected').val()
       }
       result = insert_row_quiet(payload);
       if(!result.success) return return_error(result.message);

       result = insert_services();
       if(!result.success) return return_error(result.message, 0);

       result = insert_auto_parts();
       if(!result.success) return return_error(result.message, 1);

       result = insert_payments_quota();
       if(!result.success) return return_error(result.message, 2);

       window.alert('Personalização cadastrada com sucesso!');
       return window.location.href="/nova-personalizacao";
   }

   function insert_row_quiet(payload){
      var result;
      $.ajax({
          url: "/insert",
          type: "get",
          data: payload,
          async: false,
          success: function(response) {
            if(response.status == 'error'){
                result = {
                    'success': false,
                    'message': response.message
                }
            }
            else result = { 'success': true }
          },
          error: function(response) {
                result = {
                    'success': false,
                    'message': response.message
                }
          }
       });

      return result;
   }

   function delete_row_quiet(table_name, column, id){
       $.ajax({
          url: "/delete",
          type: "get",
          data: {
            table: table_name,
            column: column,
            id: id
          },
          success: function(response) {
            console.log();
          },
          error: function(response) {
            console.log();
          }
       });
   }

   function return_error(message, tables){
      tables = ['personalizacoes', 'personalizacoes_servicos', 'personalizacoes_pecas']

      for(var x=tables; x>=0; x--) {
        console.log('delete' + x)
        delete_row_quiet(tables[x], 'cod_personalizacao', get_max_tunning_id());
      }
      window.alert('Erro ao salvar personalizacão:\n'+message)
   }

   function insert_services(){
        var result;
        $("#tbody > tr").each(function() {
           $this = $(this);
           var service_id = $this.find(".service").attr('id');
           var mechanic_id = $this.find(".mechanic").attr('id');

           var payload = {
                'table': 'personalizacoes_servicos',
                'cod_personalizacao': get_max_tunning_id(),
                'no_quotes': get_max_tunning_id(),
                'cod_servico': service_id,
                'cod_mecanico': mechanic_id
           }

           result = insert_row_quiet(payload);
           if(!result.success) return result;

        });
        return result;
   }

   function insert_auto_parts(){

        $("#tbody2 > tr").each(function() {
           $this = $(this);
           var part_id = $this.find(".part").attr('id');

           var payload = {
                'table': 'personalizacoes_pecas',
                'cod_personalizacao': get_max_tunning_id(),
                'no_quotes': get_max_tunning_id(),
                'cod_peca': part_id
           }

           result = insert_row_quiet(payload);
           if(!result.success) return result;

        });

        return result;
   }

   function insert_payments_quota() {
        total_value = parseFloat($('#tunning-value').text());
        quota = $('#quota-quantity').val()
        quota_value = total_value / quota;

        for(var x=1; x<=quota; x++){
           var due_date = new Date($(':input[type="date"]').val());

           var payload = {
                'table': 'contas_receber',
                'cod_personalizacao': get_max_tunning_id(),
                'no_quotes': get_max_tunning_id(),
                'valor_parcela': quota_value,
                'num_parcela': x,
                'total_parcelas': quota,
                'cpf_cliente': $('#customer').children('option:selected').val(),
                'data_vencimento': due_date.addDays(30*x)
           }
           if(x>1){
                delete payload.cod_personalizacao
                max_ids = `
                    ${get_max_receivable_id()},
                    ${get_max_tunning_id()}
                `
                payload['cod_recebimento, cod_personalizacao'] = max_ids
                payload['no_quotes'] = max_ids
           }

           result = insert_row_quiet(payload);
           if(!result.success) return result;
        }

        return result;
   }

   Date.prototype.addDays = function(days) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date_format(date);
   }

   function date_format(date) {
        const dateTimeFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'short', day: '2-digit' })
        const [{ value: month },,{ value: day },,{ value: year }] = dateTimeFormat .formatToParts(date )
        return `${day}-${month}-${year }`
   }

   function get_max_tunning_id(){
       return '(SELECT LAST_VALUE FROM personalizacoes_cod_personalizacao_seq)'
   }

   function get_max_receivable_id(){
       return '(SELECT LAST_VALUE FROM contas_receber_cod_recebimento_seq)'
   }
