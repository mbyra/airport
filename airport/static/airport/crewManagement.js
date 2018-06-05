// This function is called to authenticate user by the server, then display success message and fill divs in navbar for
// this user (hello message etc)
function login(from_button) {
    $.post('/crew/login/', {
        username: window.localStorage.getItem("username"),
        password: window.localStorage.getItem("password"),
    }, () => {
        $('#greeting').css('display', "").text('Logged in as ' + window.localStorage.getItem("username"));
        $('#id_logout_button').css('display', "");
        $('#id_assign_button').attr("class", "btn btn-primary");


        $('#login_panel').css("display", "none");
    }).fail(() => {
        console.log("NIE UDALO SIE ZALOGOWAC, JESTEM W LOGIN()");
        $('#greeting').css('display', "").text("Not logged in (management).");
        $('#id_logout_button').css("display", "none");
        $('#id_assign_button').attr("class", "btn btn-primary disabled");

        $('#login_panel').css("display", "");

        if (from_button === false) {
            console.log("JESTEM W FROM BUTTON FALSE");
            $('#id_alert_panel')
                .attr("class", "alert alert-info alert-dismissible text-center justify-content-center")
                .append('<button type="button" class="close" data-dismiss="alert">&times;</button>Please sign in to assign crews. You can use the same account as for main airport app, but session system in crew management app is static and <strong>completely independent</strong> from airport app (e.g. you can be signed in into different accounts in two apps).');
        } else {
            //TODO nie widać, bo ciagle robi document.ready
            console.log("JESTEM W FROM BUTTON TRUE");
            $('#id_alert_panel')
                .attr("class", "alert alert-info alert-dismissible text-center justify-content-center mt-5")
                .append('<button type="button" class="close" data-dismiss="alert">&times;</button>Username or password invalid.');
        }
        return false;
    });
}

function login_button_clicked() {
    window.localStorage.setItem("username", $('#id_login_username').val());
    window.localStorage.setItem("password", $('#id_login_password').val());
    console.log("NIE UDALO SIE ZALOGOWAC, JESTEM W LOGIN BUTTON CLICKED");

    login(true)
}

function logout_button_clicked() {
    window.localStorage.removeItem("username");
    window.localStorage.removeItem("password");

    $('#greeting').css('display', "").text("Not logged in (management).");
    $('#id_logout_button').css('display', "none");
    $('#login_panel').css("display", "");
    $('#id_alert_panel')
        .attr("class", "alert alert-success alert-dismissible text-center justify-content-center")
        .append('<button type="button" class="close" data-dismiss="alert">&times;</button>Logged out.');
}

function get_all_flights_list() {

    // console.log("jestem w get_flight_list (js)");
    // let input = prompt("jestem w get_flight_list (js)", "");

    $('#id_flight_select').empty();

    $.ajax({
        type: 'get',
        url: '/crew/get_flight_and_crew_lists/',
        // data: {
        //     year: selected_date.slice(0, 4),
        //     month: selected_date.slice(5, 7),
        //     day: selected_date.slice(8, 10),
        // },
        success: result => {
            result['flights'].forEach(flight => {

                    let id = "flight_" + flight.pk;
                    let name = "flight no " + flight.pk;
                    let source = flight.source;
                    let departure_time = flight.departure_time.slice(0, 10) + " " + flight.departure_time.slice(11, 19);
                    let destination = flight.destination;
                    let arrival_time = flight.arrival_time.slice(0, 10) + " " + flight.arrival_time.slice(11, 19);

                    $('#id_flight_select').append(
                        '<option id="' + id + '">' + name +
                        ' from ' + source + ' ' + departure_time +
                        ' to ' + destination + ' ' + arrival_time + '</option>');
                }
            );
            result['crews'].forEach(crew => {

                    $('#id_crew_select').append(
                        '<option id="crew_"' + crew.pk + '>Crew of captain ' + crew.captain_first_name + ' '
                        + crew.captain_last_name + '</option>');
                }
            );
        },
        error: function () {
            console.log("fail w get flight list");
        }
    });

}

function get_filtered_flights_list() {
    console.log("jestem w get_filtered_flight_list (js)");
    // let input = prompt("jestem w get_flight_list (js)", "");

    let selected_day = $('#id_input_date').val();
    $('#id_flight_select').empty();

    $.ajax({
        type: 'get',
        url: '/crew/get_flight_and_crew_lists/',
        data: {
            year: selected_day.slice(0, 4),
            month: selected_day.slice(5, 7),
            day: selected_day.slice(8, 10),
        },
        success: result => {
            result['flights'].forEach(flight => {

                    let id = "flight_" + flight.pk;
                    let name = "flight no " + flight.pk;
                    let source = flight.source;
                    let departure_time = flight.departure_time.slice(0, 10) + " " + flight.departure_time.slice(11, 19);
                    let destination = flight.destination;
                    let arrival_time = flight.arrival_time.slice(0, 10) + " " + flight.arrival_time.slice(11, 19);

                    $('#id_flight_select').append(
                        '<option id="' + id + '">' + name +
                        ' from ' + source + ' ' + departure_time +
                        ' to ' + destination + ' ' + arrival_time + '</option>');
                }
            );
            result['crews'].forEach(crew => {

                    $('#id_crew_select').append(
                        '<option id="crew_"' + crew.pk + '>Crew of captain ' + crew.captain_first_name + ' '
                        + crew.captain_last_name + '</option>');
                }
            );
        },
        error: function () {
            console.log("fail w get flight list");
        }
    });
}

// Page logic:
function assign_crew() {
    let flight_pk = $("#id_flight_select").val().split(" ")[2];
    let crew = $("#id_crew_select").val().split(" ").slice(3, 5);
    console.log("flight_pk: ", flight_pk, "crew: ", crew);

    $.ajax({
        type: 'post',
        url: '/crew/assign_crew/',
        data: {
            username: window.localStorage.getItem('username'),
            password: window.localStorage.getItem('password'),
            flight_pk: flight_pk,
            captain_first_name: crew[0],
            captain_last_name: crew[1],
        },
        success: () => {
            console.log("Success in assign crew post");
            $('#id_alert_panel')
                .empty().text("")
                .attr("class", "alert alert-success alert-dismissible text-center justify-content-center")
                .append('<button type="button" class="close" data-dismiss="alert">&times;</button>Successfully assigned crew to flight.');
        },
        error: () => {
            console.log("Failure in assign crew post");
            $('#id_alert_panel')
                .empty().text("")
                .attr("class", "alert alert-warning alert-dismissible text-center justify-content-center")
                .append('<button type="button" class="close" data-dismiss="alert">&times;</button>Could not assign crew to this flight - they already have a flight in this time.');
        }
    })
}

// let pageInitialized = false; // flag to run document.ready only once
jQuery(document).ready(() => {
    console.log("ROZPOCZYNAM DOCUMENT.READY");
    // if (pageInitialized) return;
    // pageInitialized = true;
    // if user is logged in (in local storage), then display logged user panel for him:
    login(false);
    // get_all_flights_list();

    $('#id_login_button').click(login_button_clicked);
    $('#id_logout_button').click(logout_button_clicked);
    $('#id_select_day_button').click(get_filtered_flights_list);
    $('#id_assign_button').click(assign_crew);

});