$(document).ready(register_events)

function register_events() {
    register_song_details();
    register_submit_add_song();

}

function register_song_details() {
    song_details = $('.song_details:not(#todays_song_details)');
    song_details.css('height', 25, 'important');
    song_details.css('overflow', 'hidden');
    song_details.click(function (e) {
    song_details = $(e.target).closest('.song_details')
    current_height = song_details.height()
    if(song_details.height() == 25) {
        to_height = song_details.css('height', 'auto').height();
    }
    else {
        to_height = 25;
    }
    song_details.height(current_height).animate({height: to_height}, 500);});
}

function register_submit_add_song() {
    $('#add_song_submit').click(function() {
        $('#song_date').attr('value', $('#date_selection').text());
        test = $("<img src='http://drupal.org/files/54640843-ajax-style-loading-gif-animation.gif' />");

        $('#form_container').append(test);
    });
}
