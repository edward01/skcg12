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
// function disable_fields(disabled) {
// 	$form.find('input, textarea, select').prop('disabled', disabled);
// 	$("html, body").animate({
// 		scrollTop: 0
// 	}, 'fast');
// }

function gotoTop() {
	$("html, body").animate({
		scrollTop: 0
	}, 'fast');
}


//- ajax post (show loader)
function ajax_post(url_action, params, success_msg, success_func, always_func) {
    toastr.clear();
    toggle_loader(true);
    $.post(url_action, params, function(resp) {
        if (resp.hasOwnProperty('error')) {
            toastr.error(resp.error, "Process failed.", {timeOut: 120000});
        }
        else {
            toastr['success'](success_msg);
            success_func(resp);
        }
    })
    .fail(function() {
        toastr.error('Please try again later.', "Server Error", {timeOut: 120000});
    })
    .always(function() {
        always_func();
        toggle_loader(false);
    });
}

//- ajax post2 (no loader; disable fields, buttons)
function ajax_post_form($frmProcess, success_msg, success_func, always_func) {
    toastr.clear();
	var origBtnHtml = $frmProcess.find('button[type="submit"]').html();
    var serialized = $frmProcess.serialize();
    $frmProcess.find('input, button').prop('disabled', true);
    $frmProcess.find('button[type="submit"]').html('Processing...');
    $.post($frmProcess.attr('action'), serialized, function(resp) {
        if (resp.hasOwnProperty('error')) {
            toastr.error(resp.error, "Process failed.", {timeOut: 120000});
        }
        else {
            toastr['success'](success_msg);
            success_func(resp);
        }
    })
    .fail(function() {
        toastr.error('Please try again later.', "Server Error", {timeOut: 120000});
    })
    .always(function() {
        always_func();
        $frmProcess.find('input, button').prop('disabled', false);
        $frmProcess.find('button[type="submit"]').html(origBtnHtml);
    });
}

// //- ajax post3 (file upload)
// function ajax_post_file($frmProcess, success_msg, success_func, always_func) {
//     toastr.clear();
// 	var origBtnHtml = $frmProcess.find('button[type="submit"]').html();
//     // var serialized = $frmProcess.serialize();
// 	var serialized = new FormData($frmProcess[0]);
//     $frmProcess.find('input, button').prop('disabled', true);
//     $frmProcess.find('button[type="submit"]').html('Processing...');
//     $.post($frmProcess.attr('action'), serialized, function(resp) {
//         if (resp.hasOwnProperty('error')) {
//             toastr.error(resp.error, "Process failed.", {timeOut: 120000});
//         }
//         else {
//             toastr['success'](success_msg);
//             success_func(resp);
//         }
//     })
//     .fail(function() {
//         toastr.error('Please try again later.', "Server Error", {timeOut: 120000});
//     })
//     .always(function() {
//         always_func();
//         $frmProcess.find('input, button').prop('disabled', false);
//         $frmProcess.find('button[type="submit"]').html(origBtnHtml);
//     });
// }


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
        gotoTop();
        return false;
    });

});
