$(document).ready(function () {
    // var value_axial = Slider(lbl_axial, slider_axial, value_axial)
    var value_axial = 256
    $("#lbl_axial").text("Axial " + value_axial)
    $("#slider_axial").slider({
        min: 1,
        max: 512,
        step: 1,
        value: value_axial,
        slide: function (event, ui) {
            $("#lbl_axial").text("Axial " + ui.value)
            value_axial = ui.value

            // sendAjax(ui.value, axialNumber)

            $.ajax({
                url: '/showDicom',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    axialNumber: value_axial,
                    type: "dicom_show"
                }),
                success: function (response) {
                    $('#axial_image').attr('src', response.img);
                }
            })
        }
    })

    var value_sagital = 256
    $("#lbl_sagital").text("Sagital " + value_sagital)
    $("#slider_sagital").slider({
        min: 1,
        max: 512,
        step: 1,
        value: value_sagital,
        slide: function (event, ui) {
            $("#lbl_sagital").text("Sagital " + ui.value)
            value_sagital = ui.value

            // sendAjax(ui.value, axialNumber)

            $.ajax({
                url: '/showDicom',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    sagitalNumber: value_sagital,
                    type: "dicom_show"
                }),
                success: function (response) {
                    $('#sagital_image').attr('src', response.img);
                }
            })
        }
    })

    var value_coronal = 256
    $("#lbl_coronal").text("Coronal " + value_coronal)
    $("#slider_coronal").slider({
        min: 1,
        max: 512,
        step: 1,
        value: value_coronal,
        slide: function (event, ui) {
            $("#lbl_coronal").text("Coronal " + ui.value)
            value_coronal = ui.value

            // sendAjax(ui.value, axialNumber)

            $.ajax({
                url: '/showDicom',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    coronalNumber: value_coronal,
                    type: "dicom_show"
                }),
                success: function (response) {
                    $('#coronal_image').attr('src', response.img);
                }
            })
        }
    })
    // $(".btn").click(function () {
    //     $.ajax({
    //         type: "POST",
    //         url: "/showDicom",
    //         contentType: "application/json",
    //         data: JSON.stringify({
    //             type: "dicom_segmentation"
    //         }),
    //         success: function (response) {
    //             value_axial = 1
    //         }

    //     })
    // });
    // $('#form_axial').on('submit', function (e) {
    //     sendAjax("axialNumber", value_axial, "axial_image");
    //     e.preventDefault();
    // })
})

// function sendAjax(value, typeImg) {
//     $("#lbl_axial").text(ui.value)
//     value_axial = ui.value
//     $.ajax({
//         url: '/showDicom',
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify({
//             [value]: value
//         }),
//         success: function (response) {
//             $('#' + typeImg).attr('src', response.img);
//         }
//     })
// }




// function sendAjax(typeNumber, value, typeImg) {
//     var number = typeNumber
//     $.ajax({
//         url: '/showDicom',
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify({
//             [number]: value
//         }),
//         success: function (response) {
//             $('#' + typeImg).attr('src', response.img);
//         }
//     })

// }

 // $('#form_axial').on('submit', function (e) {
    //     $.ajax({
    //         url: '/showDicom',
    //         type: "POST",
    //         contentType: "application/json",
    //         //data: { number: value_axial },
    //         data: JSON.stringify({
    //             number: value_axial
    //         }),
    //         success: function (response) {
    //             $('img').attr('src', response.img);
    //         }
    //     })
    //     e.preventDefault()
    // })