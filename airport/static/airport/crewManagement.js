// This function is called to authenticate user by the server, then display success message and fill divs in navbar for
// this user (hello message etc)
function login() {
    $.post('/crew/login/', {
        username: window.localStorage.getItem("username"),
        password: window.localStorage.getItem("password"),
    }, () => {
        $('#greeting').append(`Logged in as ${window.localStorage.getItem("username")}.`);
        $('#panel_for_logged_in').css("display", "");
        $('#login_panel').css("display", "none");
    }).fail(() => {
        console.log("NIE UDALO SIE ZALOGOWAC, JESTEM W LOGIN()");
        return false;
    });
}

function login_button_clicked() {
    window.localStorage.setItem("username", $('#id_login_username').val());
    window.localStorage.setItem("password", $('#id_login_password').val());
    console.log("NIE UDALO SIE ZALOGOWAC, JESTEM W LOGIN BUTTON CLICKED");

    if (login() === false) {
        console.log("NIE UDALO SIE ZALOGOWAC, JESTEM W LOGIN BUTTON CLICKED W IF");
        $('#id_alert_panel')
            .attr("class", "alert alert-danger text-center justify-content-center mt-5")
            .text("Username or password invalid.");
    }
}

function logout_button_clicked() {
    window.localStorage.removeItem("username");
    window.localStorage.removeItem("password");

    $('#greeting').empty();
    $('#panel_for_logged_in').css("display", "none");
    $('#login_panel').css("display", "");
    $('#id_alert_panel')
        .attr("class", "alert alert-success text-center justify-content-center")
        .text("Logged out.");
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
// let pageInitialized = false; // flag to run document.ready only once
jQuery(document).ready(() => {
    console.log("ROZPOCZYNAM DOCUMENT.READY");
    // if (pageInitialized) return;
    // pageInitialized = true;
    // if user is logged in (in local storage), then display logged user panel for him:
    login();
    // get_all_flights_list();

    $('#id_login_button').click(login_button_clicked);
    $('#id_logout_button').click(logout_button_clicked);
    $('#id_select_day_button').click(get_filtered_flights_list);
    // $('#id_table_flights').on('click', '.clickable-row', function (event) {
    //     $(this).addClass('active').siblings().removeClass('active');
    // });
    // $('#id_table_crews').on('click', '.clickable-row', function (event) {
    //     $(this).addClass('active').siblings().removeClass('active');
    // });


});