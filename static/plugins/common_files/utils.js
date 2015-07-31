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

//- sweet alert popups
function showConfirm(title, text, callback_func) {
	swal({
		title: title,
		text: text,
		type: "warning",
		showCancelButton: true,
		confirmButtonColor: "#d9534f",
		confirmButtonText: "Yes",
		cancelButtonText: "No"
	}, function(){
		callback_func()
	});
}
function showAlert(title, text, callback_func) {
	swal({
		title: title,
		text: text,
		type: "info"
	}, function(){
		callback_func()
	});
}

function setFocus() {
	$('form').find('input[type="text"], textarea').first().focus();
}

//-----------------
//-- MAIN
//-----------------
$(function() {
	//- sets focus
	setFocus();

	//- toastr settings
	toastr.options = {
		"positionClass": "toast-top-right",
		"onclick": null,
	}

	//- sweet alert settings


	//- bootstrap toggle (checkbox) settings

	//- scroll up feature
	//- http://answers.squarespace.com/questions/6003/how-can-i-add-a-scroll-to-top-button
	$(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });
    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 'fast');
        return false;
    });

});
