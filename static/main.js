$(document).ready(function(){
    setInterval(function(){get_lyrics();}, 2000);

    $("#set_id").on('click', function() {
        document.cookie = `id=${$('#id').val()}`;
    });
});

function get_lyrics(){
    $.post("/lyrics",  { old_song_name: localStorage.getItem("old_song_name") }, (data) => {
        if (data.status == 'new') {
            localStorage.setItem("old_song_name", data.song);
            window.scrollTo(0, 0);
            $(".lyrics").html(data.lyrics);
        }
        else {
            console.log(data.status);
        }
    });
}
