$('#login').click(function() {
                    var login_container = $('#login').parent();
                    var login_button = $('#login').detach();
                    var action = login_button.attr('current') + "/login"
                    var login_form = '<form id="login_form" action="' + action + '" method=post class="navbar-form">' +
                                        '<input id="username" name="username" type="text" value="Username" class="span2">' +
                                        '<input id="password" name="password" type="password" value="Password" class="span2">' +
                                        '<button type="submit" class="btn btn-primary">Login</button>' +
                                      '</form>';

                    login_container.append(login_form);
                    $('#username').focus(function() { $(this).attr('value', ''); });
                    $('#password').focus(function() { $(this).attr('value', ''); });
                    });

