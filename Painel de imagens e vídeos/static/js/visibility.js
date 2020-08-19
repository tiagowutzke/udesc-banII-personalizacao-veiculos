    // COMPONENT VISIBILITY CONTROLS
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

   function edit_file(edit_mode, index){
       to_show = ['#delete'+index, '#edit'+index, '#card-title-'+index, '#card-subject-'+index];
       to_hide = ['#cancel'+index, '#save'+index, '#edit-description-'+index, '#subjects-'+index];

       if(edit_mode){
            tmp = to_hide;
            to_hide = to_show;
            to_show = tmp;
       }

       to_show.forEach(show);
       to_hide.forEach(hide);
   }

   function show(element){ $(element).show(); }
   function hide(element){ $(element).hide(); }


