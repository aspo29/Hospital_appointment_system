(function ($) {
    $.fn.tablemanager = function (options = null) {
        var Table = $(this),
            tbody = $(this).find("tbody"),
            rows = $(this).find("tbody tr"),
            rlen = rows.length;

        var pagination = options !== null && options.pagination == true ? true : false;

        var currentPage = 0;
        var numPerPage = pagination ? (options.numPerPage || 5) : rows.length;
        var numOfPages = options.numOfPages !== undefined && options.numOfPages > 0 ? options.numOfPages : 5;

        function paginate(curPage = null, perPage = null) {
            var curPage = curPage === null ? currentPage : curPage;
            var perPage = perPage === null ? numPerPage : perPage;
            Table.on("paginating", function () {
                $(this)
                    .find("tbody tr")
                    .hide()
                    .slice(curPage * perPage, (curPage + 1) * perPage)
                    .show();
            });
            Table.trigger("paginating");
        }

        function appendPageControllers(nPages) {
            $("#pagesControllers").remove();
            var pagesDiv = '<nav aria-label="Page navigation example"><ul id="pagesControllers" class="pagination justify-content-center"></ul></nav>';
            Table.after(pagesDiv);

            $("#pagesControllers").append('<li class="page-item"><a class="page-link" href="#" value="first" aria-label="First"><span aria-hidden="true">&laquo;&laquo;</span></a></li>');
            $("#pagesControllers").append('<li class="page-item"><a class="page-link" href="#" value="prev" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>');

            for (var i = 1; i <= nPages; i++) {
                $("#pagesControllers").append('<li class="page-item"><a class="page-link" href="#" value="' + i + '">' + i + '</a></li>');
            }

            $("#pagesControllers").append('<li class="page-item"><a class="page-link" href="#" value="next" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>');
            $("#pagesControllers").append('<li class="page-item"><a class="page-link" href="#" value="last" aria-label="Last"><span aria-hidden="true">&raquo;&raquo;</span></a></li>');

            $(".page-link").on("click", function (e) {
                e.preventDefault();
                var value = $(this).attr("value");
                if (value == "first") {
                    currentPage = 0;
                } else if (value == "last") {
                    currentPage = numPages - 1;
                } else if (value == "prev") {
                    if (currentPage != 0) {
                        currentPage = currentPage - 1;
                    }
                } else if (value == "next") {
                    if (currentPage != numPages - 1) {
                        currentPage = currentPage + 1;
                    }
                } else {
                    currentPage = value - 1;
                }
                paginate(currentPage, numPerPage);
                $(".page-item").removeClass("active");
                $(".page-item").eq(currentPage + 2).addClass("active");

                filterPages();
            });

            filterPages();
        }

        function filterPages() {
            $(".page-item")
                .hide()
                .filter(function (i) {
                    let mid = Math.ceil(numOfPages / 2);
                    if (currentPage < mid) {
                        return i < numOfPages + 2;
                    } else if (currentPage > (numPages - (numOfPages - 1))) {
                        return i >= numPages - numOfPages + 2;
                    } else {
                        if (numOfPages % 2 == 0) {
                            return i >= currentPage - mid + 2 && i < currentPage + mid + 2;
                        } else {
                            return i > currentPage - mid + 1 && i < currentPage + mid + 2;
                        }
                    }
                })
                .show();
        }

        if (pagination) {
            var numPages = Math.ceil(rows.length / numPerPage);
            appendPageControllers(numPages);
            $(".page-item").eq(2).addClass("active");
            paginate(currentPage, numPerPage);
        }

        var filterDiv = '<div id="filterDiv" class="filterDiv" style="display: inline-block;  margin-bottom: 10px;"><label>Search: <input id="filter_input" type="text" class="form-control d-inline-block" style="width: auto;" placeholder="Type here to search..."></label></div>';
        $(this).before(filterDiv);

        $("input#filter_input").on("keyup", function () {
            var val = $.trim($(this).val()).toLowerCase();
            var isNumber = !isNaN(val) && val !== '';

            Table.find("tbody tr")
                .show()
                .filter(function () {
                    var text = $(this).text().toLowerCase();
                    if (isNumber) {
                        return !text.includes(val);
                    } else {
                        return !~text.indexOf(val);
                    }
                })
                .hide();

            if (val === '') paginate();
        });
    };
})(jQuery);

// Initialize the tablemanager with pagination and filter options
$('.tablemanager').tablemanager({
    pagination: true,
    numPerPage: 5,
    numOfPages: 5
});
