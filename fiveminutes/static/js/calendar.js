calendar = $('#calendar_toggle')

calendar.popover({'content': "<div id='calendar_popover'></div>",
                  'trigger': 'toggle',
                  'placement': 'bottom',
                  'html': true}).click(function(e) {
                                            // Bootstrap is currently broken: https://github.com/twitter/bootstrap/pull/5768
                                            // The following is a workaround until $(this).popover('toggle'); works again
                                            if ($(this).next().hasClass('in')) {
                                                $(this).popover('hide');
                                            }
                                            else {
                                                $(this).popover('show');
                                            }

                                            // Relative location of the toggle.
                                            toggle_location = $('#calendar_toggle').position()
                                            calendar = $('#calendar_popover');
                                            popover_inner = calendar.closest('.popover');
                                            popover_inner.css('left', toggle_location.left - 181);
                                            popover_inner.width('auto');
                                            popover_inner.children('.popover-title').remove();
                                            calendar.datepicker({
                                                inline: true,
                                                firstDay: 1,
                                                showOtherMonths: true,
                                                dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                                                onSelect: function(dateText, inst) {
                                                    $('#date_selection').text(dateText);
                                                    $('#calendar_toggle').popover('hide');
                                                }
                                            });
                                            calendar.datepicker({ });
                                     });
