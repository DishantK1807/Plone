
(function($){

module("CMFPlone inline-edit", {

    setup: function() {
        var self = this;

        // Create a mock server for testing ajax.
        this.server = new MoreMockHttpServer(this.handle_ajax);

        // Start the server
        this.server.start();
    },

    teardown: function() {
        // Stop the server
        this.server.stop();
    },


    //
    // Actual mock response can be produced here.
    //
    handle_ajax: function(request, ajax_heartbeat) {
        if (request.urlParts.file == 'XXX XXX XXX') {
            request.setResponseHeader("Content-Type", "application/json; charset=UTF-8");
            if (ajax_heartbeat == 0) {
                request.receive(200, JSON.stringify([])); // XXX XXX XXX
            } else if (ajax_heartbeat == 4) {
                // simulate an error
                request.receive(500, 'Error');
            }
        } else {
            request.receive(404, 'Not Found in Mock Server');
        }
    }


});


test("Bind", function() {


});


})(jQuery);

