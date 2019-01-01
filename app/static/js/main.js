$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,today,next',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },

        views: {
            month: {
                columnFormat: 'ddd',    // Column date format set to short day name day/month
                weekNumberTitle: 'Week',
            },
            agendaWeek: {
                columnFormat: 'ddd D',    // Column date format set to short day name day/month
            }
        },

        businessHours: {
            // days of week. an array of zero-based day of week integers (0=Sunday)
            dow: [1, 2, 3, 4, 5], // Monday - Friday
            start: '07:00',
            end: '19:00',
        },

        firstDay: 1,                // First day is monday
        weekNumbers: true,          // Show week number
        slotLabelFormat: 'H:mm',    // Vertical axis time format 24 hours
        defaultView: 'agendaWeek',
        allDaySlot: false,
        navLinks: true,
        editable: false,

        events: {
            url: 'presta'
        },

        eventRender: function (event, element) {
            var ms = event.end.diff(event.start);
            var d = moment.duration(ms);
            var s = Math.floor(d.asHours()) + moment.utc(ms).format(":mm");

            element.find('.fc-time').text(moment(event.start).format('HH:mm') + " - " + moment(event.end).format('HH:mm') + " ("+ String(s) +") ");
        },

        // Events handling
        eventClick: function (calEvent, jsEvent, view) {
            ShowPrestaPoup(calEvent);
        },

        dayClick: function (date, jsEvent, view) {
            ShowAddPrestaPoup(date);
        }
    });

    $('#date').fdatepicker({
        format: 'dd/mm/yyyy hh:ii',
        weekStart: 1,
        disableDblClickSelection: true,
        leftArrow:'<<',
        rightArrow:'>>',
        pickTime: true
    });

    $('#duration').wickedpicker({
        title: 'Presta duration',
        now: "01:00",
        twentyFour: true,
        minutesInterval: 15
    });

    // Event ---------------------------------------------------------------------------------
    // Delete presta
    $('#prestaDelete').click( function(e) {
        e.preventDefault();

        var obj = {
            prestaid: $('#prestaid').val()
        };

        $.ajax({
            type: "POST",
            url: '/presta/delete',
            data: JSON.stringify(obj),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                console.log('Success' + data.message);  // display the returned data in the console.
                $('#calendar').fullCalendar('refetchEvents');
            },
            error: function (data) {
                console.log('Error' + data)  // display the returned data in the console.
            }
        });

        $('#presta').foundation('close');

        return false;
    });

    // Submit form
    $('#prestaform').submit(function (e) {
        var up = $('#prestaid').val()

        if(up == 0) {
            console.log("Add presta");
        }
        else {
            console.log("Update presta" + up);
        }

        $.ajax({
            type: "POST",
            url: ((up == 0) ? '/presta/add' : '/presta/update'),
            data: $('#prestaform').serialize(), // serializes the form's elements.
            success: function (data) {
                console.log('Success' + data.message)  // display the returned data in the console.
                $('#calendar').fullCalendar('refetchEvents');
            },
            error: function (data) {
                console.log('Error' + data)  // display the returned data in the console.
            }
        });
        e.preventDefault(); // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ presta.csrf_token._value() }}")
            }
        }
    })

    // Function -------------------------------------------------------------------------------
    function ShowAddPrestaPoup(date) {
        $('#prestaformtitle').text("Add Presta");
        $('#date').fdatepicker('update', date.format('DD/MM/YYYY HH:mm'));
        $('#duration').val("01 : 00");
        $('#project').val(0);
        $('#prestaid').val(0);
        $('#comment').val("");
        $('#travel_distance').val("0");
        $('#travel_comment').val("");

        document.getElementById('prestaDelete').style.visibility = 'hidden';
        document.getElementById('prestaSave').innerHTML = 'Save';

        $('#presta').foundation('open');
    }

    function ShowPrestaPoup(event) {
        $('#prestaformtitle').text("Presta details");
        $('#prestaid').val(event.id)

        $('#date').fdatepicker('update', event.start.format('DD/MM/YYYY HH:mm'));

        // Fetch presta additionnal info
        $.ajax({
            url: '/presta/detail',
            type: 'GET',
            data: {'prestaid':event.id},
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $('#comment').val(data.Description);
                $('#project').val(data.Project);
                $('#duration').val(data.Duration);
                $('#travel_distance').val(data.Travel_Distance);
                $('#travel_comment').val(data.Travel_Comment);
            }
        });

        // Button handling
        document.getElementById('prestaDelete').style.visibility = 'visible';
        document.getElementById('prestaSave').innerHTML = 'Update';

        $('#presta').foundation('open');
    }
});