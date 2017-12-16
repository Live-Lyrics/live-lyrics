import * as Cookies from "js-cookie";

import axios from 'axios';

import {MDCToolbar, MDCToolbarFoundation} from '@material/toolbar';
import {MDCTemporaryDrawer, MDCTemporaryDrawerFoundation, util} from '@material/drawer';

import {MDCFormField, MDCFormFieldFoundation} from '@material/form-field';
import {MDCCheckbox, MDCCheckboxFoundation} from '@material/checkbox';
import {MDCRadio, MDCRadioFoundation} from '@material/radio';

import discogsTemplate from '../templates/discogs.handlebars';
import youtubeTemplate from '../templates/youtube.handlebars';

import domready from 'domready';

import '../css/lyrsense.css';
import '../css/amalgama.css';
import '../css/main.css';

let drawer = new MDCTemporaryDrawer(document.querySelector('.mdc-temporary-drawer'));
document.querySelector('.demo-menu').addEventListener('click', () => drawer.open = true);


domready(function () {
  loadRadioState();

  $(".stored_radio").on("change", function() {
    localStorage[$(this).attr("name")] = $(this).val();
  });

  let checkboxValues = JSON.parse(localStorage.getItem("checkboxValues")) || {};
  let $checkboxes = $("#checkbox-container").find(":checkbox");

  $checkboxes.on("change", function() {
    $checkboxes.each(function() {
      checkboxValues[this.id] = this.checked;
    });
    localStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));
  });

  setInterval(() => getLyrics(), 5000);

  $("#set_id").on("click", function() {
    document.cookie = `id=${$("#id").val()}`;
  });
});

function loadRadioState () {
  $("#"+localStorage.getItem('broadcast_provider')).prop("checked", true);
  $("#"+localStorage.getItem('lyrics_provider')).prop("checked", true);

  let checkboxValues = JSON.parse(localStorage.getItem("checkboxValues"));

  $.each(checkboxValues, function(key, value) {
    $("#" + key).prop("checked", value);
  });
}

function SpotifuSetLyrics(artist, title) {
  axios
    .post("/spotify-lyrics", {
      artist: artist,
      title: title,
      lyrics_provider: localStorage.getItem("lyrics_provider"),
      additional_information: localStorage.getItem("checkboxValues")
    })
    .then(function(response) {
      if (response.data.status === "found") {
        window.scrollTo(0, 0);
        $("#lyrics").html(response.data.lyrics);

        if (response.data.discogs) {
          let discogs = discogsTemplate(response.data.discogs);
          let discogs_list = document.getElementById('discogs-list');
          discogs_list.innerHTML = discogs;
        } else {
          $("#discogs-list").html('');
        }
        if (response.data.youtube) {
          let youtube = youtubeTemplate(response.data.youtube);
          let youtube_embed = document.getElementById('youtube-embed');
          youtube_embed.innerHTML = youtube;
        } else {
          $("#youtube-embed").html('');
        }
      } else if (response.data.status === "lyrics not found") {
        console.log("lyrics not found");
      }
    });
}

function refreshToken() {
  axios
    .post("/refresh_token", {
      refresh_token: Cookies.get("refresh_token")
    })
    .then(function(response) {
      Cookies.set("access_token", response.data.access_token);
    });
}

function getCurrentPlayingTrack() {
  return axios.get("https://api.spotify.com/v1/me/player/currently-playing", {
    headers: {
      Authorization: "Bearer " + Cookies.get("access_token")
    }
  });
}

function getLyrics() {
  if (localStorage.getItem("broadcast_provider") === "spotify") {
    let currentplayingtrack = getCurrentPlayingTrack();

    currentplayingtrack
      .then(function(response) {
        let artist = response.data.item.artists[0].name;
        let title = response.data.item.name;
        let current = `${artist} ${title}`;

        if (localStorage.getItem("old_song_name") === current) {
          console.log("song not change");
        } else {
          console.log("new song");
          SpotifuSetLyrics(artist, title);
          localStorage.setItem("old_song_name", current);
        }
      })
      .catch(function(error) {
        console.log(error.request.responseText);
        refreshToken();
      });
  } else if (localStorage.getItem("broadcast_provider") === "vk") {
    console.log("vk");
    // $.post(
    //   "/vk-lyrics",
    //   { old_song_name: localStorage.getItem("old_song_name") },
    //   data => {
    //     if (data.status == "new") {
    //       localStorage.setItem("old_song_name", data.song);
    //       window.scrollTo(0, 0);
    //       $("#lyrics").html(data.lyrics);
    //     } else {
    //       console.log(data.status);
    //     }
    //   }
    // );
  }
}
