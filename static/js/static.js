$(function() {
    var btn = $(".btn-expand");
    
    btn.on('click', function(e) {
        e.preventDefault();
        $(this).siblings('.panel-body').toggleClass('panel-preview'); // toggle class
    });
});