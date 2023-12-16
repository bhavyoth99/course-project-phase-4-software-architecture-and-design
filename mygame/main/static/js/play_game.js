// js/play_game.js
$(document).ready(function() {
    // Add click event to cards to select/deselect them
    $('.card-deck .card').click(function() {
        var checkbox = $(this).find('input[type="checkbox"]');
        checkbox.prop('checked', !checkbox.prop('checked'));
        $(this).toggleClass('card-selected');
    });
});
