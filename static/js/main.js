
    // ELEMENTS VISIBILITY FUNCTIONS
    function change_fields_visibility(id, edit_mode){
        var info_fields = '.visible-field-' + id
        var edit_btn = '#edit-'   + id;
        var cancel_btn  = '#cancel-' + id
        var save_btn    = '#save-'   + id
        var delete_btn  = '#delete-' + id

        if(edit_mode){
            $(edit_btn).hide();
            $(delete_btn).hide();
            $(info_fields).hide();
            $(cancel_btn).show();
            $(save_btn).show();
            // Edit fields
            var i = 1;
            do {
                col_id = '#col' + i + '-' + id
                $(col_id).show();
                i++;
            }
            while($(col_id).length);
        }
        else{
            $(edit_btn).show();
            $(delete_btn).show();
            $(info_fields).show();
            $(cancel_btn).hide();
            $(save_btn).hide();
            // Edit fields
            var i = 1;
            do {
                col_id = '#col' + i + '-' + id
                $(col_id).hide();
                i++;
            }
            while($(col_id).length);
        }
   }

   function change_row_visibility(insert_mode){
       if(insert_mode) $('#new-row').show();
       else $('#new-row').hide();
   }

   function swap_elements_visibility(to_hide, to_show){
       $(to_show).show();
       $(to_hide).hide();
   }


   function new_option_field(combo_box, combo_id, field_id, delete_btn, hidden_id, redirect){
        selected_value = $(combo_box).children('option:selected').val();
        should_hide = selected_value == 'new-value'

        if(!should_hide){
            $(delete_btn).show();
            $(hidden_id).val(selected_value);
            return false;
        }

        if(redirect) window.open(redirect, '_blank');

        $(combo_id).hide();
        $(delete_btn).hide();
        $(field_id).show();
   }

   // DML FUNCTIONS
   function update_row(id, table_name, column, cols_quantity, column_cast){
       if (!confirm("Confirma a alteração?")) return false;

       var payload = {
            'table': table_name,
            'column': column,
            'old_id': id
        }
        if(column_cast) payload['cast'] = column_cast;

       // Append other values and columns
       for(var i=1; i<=cols_quantity; i++) {
          col_id = '#col' + i + '-' + id
          payload[$(col_id).attr('name')] = $(col_id).val()
       }

       $.ajax({
          url: "/update",
          type: "get",
          data: payload,
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao atualizar:\n' + response.message);
            else {
                window.alert('Registro atualizado com sucesso!');
                $('body').html(response);
            }
          },
          error: function(response) {
            window.alert('Erro ao atualizar:\n' + response);
          }
       });
   }

   function insert_row(table_name, cols_quantity, no_quotes){
       if (!confirm("Confirma a inserção do registro?")) return false;

       var payload = { 'table': table_name };

       if(no_quotes) payload['no_quotes'] = no_quotes;
       // Append other values and columns
       for(var i=1; i<=cols_quantity; i++) {
          col_id = '#col' + i
          payload[$(col_id).attr('name')] = $(col_id).val()
       }

       $.ajax({
          url: "/insert",
          type: "get",
          data: payload,
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao inserir:\n' + response.message);
            else {
                window.alert('Registro inserido com sucesso!');
                $("body").html(response);
            }
          },
          error: function(response) {
            if(response.status == 302){
                window.alert('Registro inserido com sucesso!');
                $("body").html(response);
            }
            else window.alert('Erro ao inserir:\n' + response);
          }
       });
   }


  function delete_row(table_name, column, id){
       if (!confirm("Confirma a exclusão do registro?")) return false;

       $.ajax({
          url: "/delete",
          type: "get",
          data: {
            table: table_name,
            column: column,
            id: id
          },
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao excluir registro:\n' + response.message);
            else {
                window.alert('Registro excluído com sucesso!');
                $('body').html(response);
            }
          },
          error: function(response) {
            window.alert('Erro ao excluir registro:\n' + response);
          }
       });
   }

   function insert_combo_value(table_name, table_pkey, column, value, combo_id){
       payload = {'table': table_name}
       payload[column] = value

       $.ajax({
          url: "/insert",
          type: "get",
          data: payload,
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao inserir registro:\n' + response.message);
            else query_combo_values(table_name, table_pkey, column, combo_id);
          },
          error: function(response) {
            window.alert('Erro ao inserir registro:\n' + response);
          }
       });
   }

  function delete_combo_value(table_name, table_pkey, column, id, combo_id){
       if (!confirm("Confirma a exclusão do registro?")) return false;

       $.ajax({
          url: "/delete",
          type: "get",
          data: {
            table: table_name,
            column: table_pkey,
            id: id
          },
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao excluir registro:\n' + response.message);
            else query_combo_values(table_name, table_pkey, column, combo_id);
          },
          error: function(response) {
            window.alert('Erro ao excluir registro:\n' + response);
          }
       });
   }

   function query_combo_values(table_name, table_pkey, column, combo_id){
       payload = {
            'table': table_name,
            'column': column,
            'pkey': table_pkey
       }
       $.ajax({
          url: "/query_combo_values",
          type: "get",
          data: payload,
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao buscar valores:\n' + response.message);
            else $(combo_id).html(response);
          },
          error: function(response) {
            window.alert('Erro ao buscar registro:\n' + response);
          }
       });
   }

   function set_checkbox_value(checkbox){
        is_checked = $(checkbox).is(":checked")
        if(is_checked) $(checkbox).val('true')
        else $(checkbox).val('false')
   }




