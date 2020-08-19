   function copy_clipboard(text_id) {
       var $temp = $("<input>");
       $("body").append($temp);
       $temp.val($(text_id).text()).select();
       document.execCommand("copy");
       $temp.remove();

       setTimeout(function() {
        $("[data-toggle='popover']").popover('hide');
       }, 2000)
   }



   function set_checkbox_value(checkbox){
        is_checked = $(checkbox).is(":checked")
        if(is_checked) $(checkbox).val('true')
        else $(checkbox).val('false')
   }

   function set_hidden_value(combo_box, input_id){
       selected_value = $('#'+combo_box.id).children('option:selected').val();
       $(input_id).val(selected_value);
   }

   function new_subject(combo_box, field_id, delete_btn){
        selected_value = $(combo_box).children('option:selected').val();
        should_hide = selected_value == 'new-value'

        if(!should_hide){
            $(delete_btn).show();
            return false;
        }

        $('#'+combo_box.id).hide();
        $(delete_btn).hide();
        $(field_id).show();
   }




