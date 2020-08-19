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

   function insert_combo_subjects_value(){
       if (!confirm("Confirma a inserção do registro?")) return false;

       var payload = {
            'table': 'subjects',
            'is_combo': 'True',
            'description': $('#new-subject-value').val()
       };

       $.ajax({
          url: "/insert",
          type: "get",
          data: payload,
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao inserir:\n' + response.message);
            else {
                window.alert('Registro inserido com sucesso!');
                $("#subjects").html(response);
            }
          },
          error: function(response) {
            if(response.status == 302){
                window.alert('Registro inserido com sucesso!');
                $("#subjects").html(response);
            }
            else window.alert('Erro ao inserir:\n' + response);
          }
       });
   }


  function delete_row(table_name, column, combo_id){
       if (!confirm("Confirma a exclusão do registro?")) return false;

       id = $(combo_id).children('option:selected').val()

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
                $(`${combo_id} option[value='${id}']`).remove();
            }
          },
          error: function(response) {
            window.alert('Erro ao excluir registro:\n' + response);
          }
       });
   }


   function delete_file(table_name, id){
       if (!confirm("Confirma a exclusão do arquivo?")) return false;

       $.ajax({
          url: "/delete_file",
          type: "get",
          data: {
            table: table_name,
            id: id
          },
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao excluir arquivo:\n' + response.message);
            else {
                window.alert('Arquivo excluído com sucesso!');
                location.reload();
                return false;
            }
          },
          error: function(response) {
            window.alert('Erro ao excluir registro:\n' + response);
          }
       });
   }


   function update_file(table_name, index, image_id){
       if (!confirm("Confirma a alteração do arquivo?")) return false;

       description = $('#edit-description-'+index).val();
       subject = $('#subject-'+index).val();

       $.ajax({
          url: "/update",
          type: "get",
          data: {
            table: table_name,
            column: 'id',
            old_id: image_id,
            description: `'${description}'`,
            subject: subject
          },
          success: function(response) {
            if(response.status == 'error')
                window.alert('Erro ao alterar o arquivo:\n' + response.message);
            else {
                $('#card-title-'+index).text(description);

                subject_text = $("#subjects-"+index+" option:selected").text();
                $('#card-subject-'+index).text(subject_text);

                edit_file(false, index);
            }
          },
          error: function(response) {
            window.alert('Erro ao alterar a imagem:\n' + response);
          }
       });
   }
