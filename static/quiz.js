"use strict";
var static_url = $("#static")[0].innerHTML;
var choice_mapping = {
    1: "ROCK",
    2: "PAPER",
    3: "SCISSORS",
    4: "SPOCK",
    5: "LIZARD",
};
var Quiz = /** @class */ (function () {
    function Quiz() {
    }
    Quiz.prototype.show_question = function () {
        $("#answeryesno").css("display", "block");
        $("#continue").css("display", "none");
        $("#results").css("display", "none");
    };
    Quiz.prototype.initialize_selection = function () {
        var thisquiz = this;
        thisquiz.show_question();
        return;
    };
    Quiz.prototype.show_results = function () {
        $("#answeryesno").css("display", "none");
        $("#continue").css("display", "block");
        $("#continuebtn")[0].focus();
        $("#results").css("display", "block");
    };
    Quiz.prototype.guess = function (choice) {
        var thisquiz = this;
        $("#results").removeClass("bg-success").removeClass("bg-danger").removeClass("bg-primary");
        $.post("/play", JSON.stringify({ "player": choice }), function (response) {
            $("#player_choice_text").html(choice_mapping[response.player]);
            $("#computer_choice_text").html(choice_mapping[response.computer]);
            if (response.results == "win") {
                $("#results_text").html("WIN");
                $("#results").addClass("bg-success");
            }
            else if (response.results == "lose") {
                $("#results_text").html("LOSE");
                $("#results").addClass("bg-danger");
            }
            else {
                $("#results_text").html("DRAW");
                $("#results").addClass("bg-primary");
            }
            thisquiz.show_results();
        });
    };
    return Quiz;
}());
var quiz = new Quiz();
$(document).ready(function () {
    quiz.initialize_selection();
    $(document).keypress(function (e) {
        if ((e.key == "Enter" || e.key == "c") && $("#continue").css("display") != "none") {
            e.preventDefault();
            $("#continuebtn").trigger("click");
        }
        else if ($("#answeryesno").css("display") != "none") {
            if (e.key == "r") {
                e.preventDefault();
                $("#rockbtn").trigger("click");
            }
            else if (e.key == "p") {
                e.preventDefault();
                $("#paperbtn").trigger("click");
            }
            else if (e.key == "s") {
                e.preventDefault();
                $("#scissorsbtn").trigger("click");
            }
            else if (e.key == "o") {
                e.preventDefault();
                $("#spockbtn").trigger("click");
            }
            else if (e.key == "l") {
                e.preventDefault();
                $("#lizardbtn").trigger("click");
            }
        }
    });
    $("#continuebtn").click(function (e) {
        e.preventDefault();
        quiz.show_question();
    });
    $("#rockbtn").click(function (e) {
        e.preventDefault();
        quiz.guess(1);
    });
    $("#paperbtn").click(function (e) {
        e.preventDefault();
        quiz.guess(2);
    });
    $("#scissorsbtn").click(function (e) {
        e.preventDefault();
        quiz.guess(3);
    });
    $("#spockbtn").click(function (e) {
        e.preventDefault();
        quiz.guess(4);
    });
    $("#lizardbtn").click(function (e) {
        e.preventDefault();
        quiz.guess(5);
    });
});
