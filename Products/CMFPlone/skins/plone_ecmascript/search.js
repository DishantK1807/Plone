var container = jq('#search-results');

jq("form.searchPage").submit(function() {
    var data = jq("form.searchPage").serialize();
    jq(container).fadeOut('fast');
    updateResults(data);
    return false;
}); 
jq("#search-filter input").bind('change', function() {
    var data = jq("form.searchPage").serialize();
    jq(container).fadeOut('fast');
    updateResults(data);
    return false;
});

function submitForm() {
    var data = jq("form.searchPage").serialize();
    jq(container).fadeOut('fast');
    updateResults(data);
    return false;                        
}

jq('#searchResultsHeading').click(function(event) {
   //jq("#search-results").fadeOut(300);
   if (jq(event.target).is('#sorting-options a')) {
       if (jq(event.target).attr('rel')) {
           rel = jq(event.target).attr('rel');                               
           jq("form.searchPage input[name='sort_on']").val(rel);                               
       }
       else {
           jq("form.searchPage input[name='sort_on']").val("");
       }
       var data = jq("form.searchPage").serialize();   
       updateResults(data);
       // jq("#search-results").before(jq("#kssPortalMessage"));
       // jq("#kssPortalMessage dd").html("Your search results have been updated");
       // 
       // jq("#kssPortalMessage").delay(500).animate({
       //     height: ['toggle', 'swing'],
       //     opacity: 1,
       //     marginBottom: 'toggle',
       //     marginTop: 'toggle'
       // }, 500, function(){
       //     jq("*").click(function(){
       //         jq("#kssPortalMessage").fadeOut('slow');
       //     })
       // })
       return false;
   }
 });


function updateResults(data){
    jq.ajax({
        url: '@@updated_search',
        data: data,
        success: function(data){
            container.hide();
            container.html(data);
            jq(container).fadeIn('medium');
            jq("#search-results-number").text(function(){
                str = jq("#updated-search-results-number").text();
                jq("#updated-search-results-number").remove();
                return str;
            });
            jq("#searchResultsHeading #sorting-options").html(function(){
                struct = jq("#updated-sorting-options").html();
                jq("#updated-sorting-options").remove();
                return struct;
            });  
        },
        error: function(req,error){
            if(error === 'error'){error = req.statusText;}
            var errormsg = 'There was a communication error: ' + error;
            container.html(errormsg);
        }
    });
}                    

jq('#show-search-options').click(function () {                        
    jq("#search-results-wrapper").css({"width":"97.75%", "margin-left":"-98.875%"});
    jq("#search-results-wrapper").removeClass("width-16");
    jq("#search-results-wrapper").removeClass("position-0");
    jq('#search-filter').hide();
    jq('#search-filter').removeClass('hiddenStructure');
    
    jq("#search-results-wrapper").animate({
        width: '72.75%',
        marginLeft: '-73.875%'
    }, 500, function(){
        jq('#search-filter').fadeIn('medium');
        jq("#show-search-options").delay(500).fadeOut();
    });
    jq("#search-results-wrapper").addClass("position-1:4");
    jq("#search-results-wrapper").addClass("width-12");                        
    return false;
});