function update_cost() {
    it_price = jQuery('#instance_types option:selected').attr('price');
    db_price = jQuery('#database_types option:selected').attr('price');
    ppd = (parseFloat(it_price) * 24) + (parseFloat(db_price) * 24);
    ppd= parseFloat(ppd).toFixed(2);
    jQuery('#per_day').html('$' + ppd);
}

function build_instance_table(json_request) {
    jQuery('#instance_tbody').empty();
    jQuery.each(json_request, function(index, row) {
        if (row.building !== "False") {
            row.state = 'Building';
        } else if (row.running === "True") {
            row.state = 'Running';
        } else {
            row.state = 'Not Running';
        }
        table_row = jQuery("<tr/>", { 'html': "" });
        td1 = jQuery("<td/>", { "html": "" });
        if (row.public_dns_name === 'None') {
            a = jQuery("<a/>", { "html": row.name, "href": "#" });
        } else {
            a = jQuery("<a/>", { "html": row.name, "target": "_BLANK", "href": "https://" + row.public_dns_name });
        }
        td1.append(a);
        td2 = jQuery("<td/>", { "html": row.state });
        td3 = jQuery("<td/>", { "html": row.size });
        td4 = jQuery("<td/>", { "html": "" });
        table_row.append(td1);
        table_row.append(td2);
        table_row.append(td3);

        // console.log(row);
        if (row.state !== 'Building') {
            if (row.state === 'Running') {
                shutdown = jQuery("<a/>", {"href": "/shutdown/" + row.id, "class": "btn btn-small btn-warning", "html": "Stop", "style": "margin-right: 10px" });
                td4.append(shutdown);
            }
            else {
                start = jQuery("<a/>", {"href": "/start/" + row.id, "class": "btn btn-small btn-success", "html": "Start", "style": "margin-right: 10px" });
                td4.append(start);
            }
            terminate = jQuery("<button/>", {"instance_id": row.id, "class": "delete-instance btn btn-small btn-danger", "html": "Delete", "style": "margin-right: 10px" });
            td4.append(terminate);
        } else {
            spinner = jQuery("<img/>" , {"src": "/static/img/spinner.gif"});
            td4.append(spinner);
        }
        table_row.append(td4);
        if (row.state === 'Not Running') {
            table_row.addClass('error');
        }
        if (row.state === 'Running') {
            table_row.addClass('success');
        }
        if (row.state === 'Building') {
            table_row.addClass('warning');
        }
        jQuery('#instance_tbody').append(table_row);
    });
    return true;
}

function randomString(L){
    var s = '';
    var randomchar = function() {
        var n = Math.floor(Math.random()*62);
        if (n < 10) {
            return n; //1-10
        }
        if (n < 36) {
            return String.fromCharCode(n+55); //A-Z
        }
        return String.fromCharCode(n+61); //a-z
    };
    while(s.length< L) {
        s+= randomchar();
    }
    return s;
}

(function($){
    $.fn.extend({
        handleDelete: function(options) {
            this.defaultOptions = {};

            var settings = $.extend({}, this.defaultOptions, options);

            return this.each(function() {
                var $this = $(this);
                $this.click(function(e) {
                    e.preventDefault();
                    instanceId = $(this).attr('instance_id');
                    bootbox.confirm("Are you sure you want to delete this instance? This can't be undone. There is no un-ringing that bell.", function(confirmed) {
                        if (confirmed) {
                            window.location.href = '/terminate/' + instanceId;
                        }
                    });
                });
            });
        }
    });
})(jQuery);

(function($){
    $.fn.extend({
        launchFill: function(options) {
            this.defaultOptions = {};

            var settings = $.extend({}, this.defaultOptions, options);

            return this.each(function() {
                var $this = $(this);
                $this.change(function() {
                    rs = randomString(6);
                    $instance_name = $('input[name="instance_name"]');
                    $instance_name.attr('placeholder', $this.attr('value') + '-' + rs);
                    $instance_name.attr('value', $this.attr('value') + '-' + rs);
                    $instance_name.focus();

                    $subsite_name = $('input[name="subsite_name"]');
                    $subsite_name.attr('placeholder', $this.attr('value') + '-' + rs);
                    $subsite_name.attr('value', $this.attr('value') + '-' + rs);
                    $('input[name="pull_request"]').focus();
                });
            });
        }
    });
})(jQuery);

(function($){
    $(document).on("click", ".btn-size", function(e) {
        $this = e.target;
        if ($this.id === 'button-tiny') {
            $('#instance_types option')[4].selected = true;
            $('#database_types option')[4].selected = true;
        }
        else if ($this.id === 'button-small') {
            $('#instance_types option')[0].selected = true;
            $('#database_types option')[0].selected = true;
        }
        else if ($this.id === 'button-medium') {
            $('#instance_types option')[1].selected = true;
            $('#database_types option')[1].selected = true;
        }
        else if ($this.id === 'button-large') {
            $('#instance_types option')[2].selected = true;
            $('#database_types option')[2].selected = true;
        }
        else if ($this.id === 'button-xl') {
            $('#instance_types option')[3].selected = true;
            $('#database_types option')[3].selected = true;
        }
        update_cost();
    });
    $(document).on("change", ".pricing", function(e) {
        update_cost();
    });
})(jQuery);
