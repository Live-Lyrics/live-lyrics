import * as cookie from "jquery.cookie";
import domready from "domready";

domready(function() {
  console.log("from lyrics");

  function toggleLighted(e) {
    if (e.target && e.target.classList.contains("highlightLine")) {
      let line = e.target.getAttribute("line");
      let lineCollection = document.getElementsByClassName("line" + line);
      Array.from(lineCollection).forEach(function(el) {
        el.classList.toggle("lighted");
      });
    }
  }

  document.getElementById("lyrics").addEventListener("mouseover", toggleLighted);
  document.getElementById("lyrics").addEventListener("mouseout", toggleLighted);

  function sc(nameclas, symbol) {
    console.log(nameclas);
    console.log(symbol);
    var size = $("#fr_text").css("font-size");
    var num = parseInt(size.match(/\d+/), 10);
    num = symbol === "+" ? (num += 2) : (num -= 2);
    var inter = num * 1.5;

    document.getElementById("fr_text").style.fontSize = num + "px";
    document.getElementById("fr_text").style.lineHeight = inter + "px";
    document.getElementById("ru_text").style.fontSize = num + "px";
    document.getElementById("ru_text").style.lineHeight = inter + "px";

    $.cookie("fontSize", num + "px", {
      expires: 3000000,
      path: "/"
    });
  }

  document.getElementById("lyrics").addEventListener("click", function(e) {
    if (e.target && e.target.classList.contains("fontSmaller")) {
      sc("fontSmaller", "-");
    } else if (e.target && e.target.classList.contains("fontBigger")) {
      sc("fontBigger", "+");
    }
  });

  var target = document.getElementById("lyrics");

  // create an observer instance
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      console.log(mutation.type);
      console.log(mutation);
      if ($.cookie("fontSize")) {
        var size = $.cookie("fontSize");
        var num = parseInt(size.match(/\d+/), 10);
        var inter = num * 1.5;

        document.getElementById("fr_text").style.fontSize = size;
        document.getElementById("ru_text").style.fontSize = size;

        document.getElementById("fr_text").style.lineHeight = inter + "px";
        document.getElementById("ru_text").style.lineHeight = inter + "px";
      }
    });
  });

  // configuration of the observer:
  var config = { attributes: true, childList: true, characterData: true };

  // pass in the target node, as well as the observer options
  observer.observe(target, config);
});
