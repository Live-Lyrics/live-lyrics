import $ from 'jquery';
import * as cookie from 'jquery.cookie';
import * as Cookies from "js-cookie";

import axios from 'axios';

import {MDCToolbar, MDCToolbarFoundation} from '@material/toolbar';
import {MDCTemporaryDrawer, MDCTemporaryDrawerFoundation, util} from '@material/drawer';

import {MDCFormField, MDCFormFieldFoundation} from '@material/form-field';
import {MDCCheckbox, MDCCheckboxFoundation} from '@material/checkbox';
import {MDCRadio, MDCRadioFoundation} from '@material/radio';

import discogs_template from '../templates/discogs.handlebars';
import youtube_template from '../templates/youtube.handlebars';

import '../css/lyrsense.css';
import '../css/amalgama.css';
import '../css/main.css';

let drawer = new MDCTemporaryDrawer(document.querySelector('.mdc-temporary-drawer'));
document.querySelector('.demo-menu').addEventListener('click', () => drawer.open = true);

$(document).ready(function() {
  loadRadioState();

  $(".stored_radio").on("change", function() {
    localStorage[$(this).attr("name")] = $(this).val();
  });

  let checkboxValues = JSON.parse(localStorage.getItem("checkboxValues")) || {};
  let $checkboxes = $("#checkbox-container :checkbox");

  $checkboxes.on("change", function() {
    $checkboxes.each(function() {
      checkboxValues[this.id] = this.checked;
    });
    localStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));
  });

  setInterval(function() {
    get_lyrics();
  }, 5000);

  $("#set_id").on("click", function() {
    document.cookie = `id=${$("#id").val()}`;
  });

  //  --------------- lyrsense ---------------

  $(".highlightLine").on("mouseenter mouseleave", function(event) {
    let line = $(this).attr("line");
    $(".line" + line).toggleClass("lighted");
  });

  $(".fontBigger").click(function() {
    var size = $("#fr_text").css("font-size");
    var num = parseInt(size.match(/\d+/), 10);
    num += 2;
    var inter = num * 1.5;

    $("#fr_text").css("font-size", num + "px");
    $("#fr_text").css("line-height", inter + "px");
    $("#ru_text").css("font-size", num + "px");
    $("#ru_text").css("line-height", inter + "px");

    $.cookie("fontSize", num + "px", {
      expires: 3000000,
      path: "/"
    });
  });

  $(".fontSmaller").click(function() {
    var size = $("#fr_text").css("font-size");
    var num = parseInt(size.match(/\d+/), 10);
    num -= 2;
    var inter = num * 1.5;

    $("#fr_text").css("font-size", num + "px");
    $("#fr_text").css("line-height", inter + "px");
    $("#ru_text").css("font-size", num + "px");
    $("#ru_text").css("line-height", inter + "px");

    $.cookie("fontSize", num + "px", {
      expires: 3000000,
      path: "/"
    });
  });

  if ($.cookie("fontSize")) {
    var size = $.cookie("fontSize");
    var num = parseInt(size.match(/\d+/), 10);
    var inter = num * 1.5;

    $("#fr_text").css("font-size", size);
    $("#ru_text").css("font-size", size);

    $("#fr_text").css("line-height", inter + "px");
    $("#ru_text").css("line-height", inter + "px");
  }
});

function loadRadioState () {
  $("#"+localStorage.getItem('broadcast_provider')).prop("checked", true);
  $("#"+localStorage.getItem('lyrics_provider')).prop("checked", true);

  let checkboxValues = JSON.parse(localStorage.getItem("checkboxValues"));

  $.each(checkboxValues, function(key, value) {
    $("#" + key).prop("checked", value);
  });
}

//  --------------- lyrsense ---------------

function SpotifuSetLyrics(artist, title) {
  axios
    .post("/spotify-lyrics", {
      artist: artist,
      title: title,
      lyrics_provider: localStorage.getItem("lyrics_provider"),
      additional_information: localStorage.getItem("checkboxValues")
    })
    .then(function(response) {
      if (response.data.status == "found") {
        window.scrollTo(0, 0);
        $(".lyrics").html(response.data.lyrics);

        if (response.data.discogs) {
          let discogs = discogs_template(response.data.discogs);
          let discogs_list = document.getElementById('discogs-list');
          discogs_list.innerHTML = discogs;
        } else {
          $("#discogs-list").html('');
        }
        if (response.data.youtube) {
          let youtube = youtube_template(response.data.youtube);
          let youtube_embed = document.getElementById('youtube-embed');
          youtube_embed.innerHTML = youtube;
        } else {
          $("#youtube-embed").html('');
        }
      } else if (response.data.status == "lyrics not found") {
        console.log("lyrics not found");
      }
    });
}

function refresh_token() {
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

function get_lyrics() {
  if (localStorage.getItem("broadcast_provider") == "spotify") {
    let currentplayingtrack = getCurrentPlayingTrack();

    currentplayingtrack
      .then(function(response) {
        let artist = response.data.item.artists[0].name;
        let title = response.data.item.name;
        let current = `${artist} ${title}`;

        if (localStorage.getItem("old_song_name") == current) {
          console.log("song not change");
        } else {
          console.log("new song");
          SpotifuSetLyrics(artist, title);
          localStorage.setItem("old_song_name", current);
        }
      })
      .catch(function(error) {
        console.log(error.request.responseText);
        refresh_token();
      });
  } else if (localStorage.getItem("broadcast_provider") == "vk") {
    console.log("vk");
    // $.post(
    //   "/vk-lyrics",
    //   { old_song_name: localStorage.getItem("old_song_name") },
    //   data => {
    //     if (data.status == "new") {
    //       localStorage.setItem("old_song_name", data.song);
    //       window.scrollTo(0, 0);
    //       $(".lyrics").html(data.lyrics);
    //     } else {
    //       console.log(data.status);
    //     }
    //   }
    // );
  }
}
