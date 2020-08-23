
   function insert_new_receivable(cols_quantity){
       if (!confirm("Confirma a inserção do registro?")) return false;

       var payload = {}
       for(var i=1; i<=cols_quantity; i++) {
          col_id = '#col' + i
          payload[$(col_id).attr('name')] = $(col_id).val()
       }

       $.ajax({
          url: "/insert_receivable",
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
            window.alert('Erro ao inserir:\n' + response);
          }
       });
   }
