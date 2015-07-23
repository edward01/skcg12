//- common functions and utilities (ej)
// function toggle_form_fields(disabled_val, $form) {
// 	animate_submit_button($form.find('button[type="submit"]'), disabled_val);
// 	$form.find('input, textarea, button, select').prop('disabled', disabled_val);
// }

// function animate_submit_button(btn, state) {
// 	if (state) {
// 		// btn.children().addClass('fa-spin');
// 		btn.contents().last().replaceWith(" Processing...");
// 	} else {
// 		// btn.children().removeClass('fa-spin');
// 		btn.contents().last().replaceWith(" Submit");
// 	}
// }

function toggle_loader(show_loader) {
	if (show_loader) {
		$('#div_loader').modal('show');
	} else {
		$('#div_loader').modal('hide');
	}
}


//-----------------
//-- MAIN
//-----------------
$(function() {
	//- sets focus
    $('form').find('input[type="text"], textarea').first().focus();

	//- toastr settings
	toastr.options = {
		"positionClass": "toast-top-right",
		"onclick": null,
	}

	//- sweet alert settings

	//- bootstrap toggle (checkbox) settings


	
});
