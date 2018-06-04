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

// Page logic:
jQuery(document).ready(() => {
    console.log("Jestem w document ready");
    // if user is logged in (in local storage), then display logged user panel for him:
    login();

    $('#id_login_button').click(login_button_clicked);
    $('#id_logout_button').click(logout_button_clicked);
});