$(document).ready(function () {
    $('#id_doctor').change(function () {
        var doctorId = $(this).val();
        $.ajax({
            url: '/appointment/ajax/get-specialty-by-doctor/',
            data: {
                'doctor_id': doctorId
            },
            success: function (data) {
                $('#id_specialty').html(data.html);
                // Update the specialty based on selected doctor
                if (data.selected_specialty) {
                    $('#id_specialty').val(data.selected_specialty);
                }
            }
        });
    });

    $('#id_specialty').change(function () {
        var specialtyId = $(this).val();
        $.ajax({
            url: '/appointment/ajax/get-doctor-by-specialty/',
            data: {
                'specialty_id': specialtyId
            },
            success: function (data) {
                $('#id_doctor').html(data.html);
                // Update the doctor based on selected specialty
                if (data.selected_doctor) {
                    $('#id_doctor').val(data.selected_doctor);
                }
            }
        });
    });
});
