$(document).ready(function() {
    var maxResults = 5;
    var searchContainer = $('.search-container');
    var searchResults = $('#search-results');
    var searchForm = $('#search-form');

    $('#search-input').on('input', function() {
        var input = $(this).val();
        if (input.length >= 2) {
            $.ajax({
                type: 'GET',
                url: '/search/',
                data: { 'term': input },
                success: function(data) {
                    searchResults.empty();

                    var displayedResults = Math.min(data.length, maxResults);

                    for (var i = 0; i < displayedResults; i++) {
                        var result = data[i];
                        var gameHTML = '<div class="search-result"><a href="/game/' + result.id + '/"><img src="' + result.cover + '" alt="' + result.label + '"><span class="game-details"><span class="game-title">' + result.label + '</span><span class="release-date"> ' + result.release_date + '</span></span></a></div>';
                        searchResults.append(gameHTML);
                    }

                    searchContainer.addClass('active');
                }
            });
        } else {
            searchResults.empty();
            searchContainer.removeClass('active');
        }
    });
});
