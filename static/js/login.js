$('#login').click(function() {
                    var login_container = $('#login').parent();
                    var login_button = $('#login').detach();
                    var login_form = '<form login_form" action="" method=post class="navbar-form">' +
                                        '<input id="username" name="username" type="text" value="Username" class="span2">' +
                                        '<input id="password" name="password" type="password" value="Password" class="span2">' +
                                        '<button type="submit" class="btn btn-primary">Login</button>' +
                                        '</form>';

                    login_container.append(login_form);
                    $('#username').focus(function() { $(this).attr('value', ''); });
                    $('#password').focus(function() { $(this).attr('value', ''); });
                    });

