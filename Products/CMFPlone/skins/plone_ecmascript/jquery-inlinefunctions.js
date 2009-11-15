(function($) {
    $(function(){
        addInlineValidation();
        addInlineEditing();
        addCalendarChange();
    });

    function getKSSAttr(obj, varname){
        classes = obj.attr('class').split(' ');
        classname = 'kssattr-' + varname + '-';
        for (i in classes){
            cls = classes[i];
            if(cls.indexOf(classname) >= 0){
                return cls.substring(classname.length, cls.length);
            }
        }
        
        inherited = obj.parents("[class*='" + classname + "']");
        if (inherited.length){
            return getKSSAttr(inherited, varname);
        }

        return '';
    }

    function handleKSSResponse(response){
        $(response).find('command').each(function(){
                doKSSCommand(this);
        });
    }

    function extractSelector(command){
        selector = $(command).attr('selector');
        selectorType = $(command).attr('selectorType');
        switch (selectorType){
            case 'htmlid':
                return '#' + selector;
            case 'css':
                return selector;
            default:
                return selector;
        }
    }

    function doKSSCommand(command){
        selector = extractSelector(command);
        commandName = $(command).attr('name');
        switch (commandName){
            case 'clearChildNodes':
                $(selector).empty();
                break;
            case 'focus':
                $(selector).focus();
                break;            
            case 'replaceHTML':
                html = $(command).find('param[name="html"]').text();
                $(selector).replaceWith(html);
                break;
            case 'replaceInnerHTML':
                html = $(command).find('param[name="html"]').text();
                $(selector).html(html);
                break;
            case 'setAttribute':
                attributeName = $(command).find('param[name="name"]').text();
                replaceText = $(command).find('param[name="value"]').text();
                $(selector).attr(attributeName, replaceText);   
                break;
            case 'setStyle':
                name = $(command).find('param[name="name"]').text();
                value = $(command).find('param[name="value"]').text();
                $(selector).css(name, value);
                break;
            default:
                if (console) {
                    console.log('No handler for command ' + $(command).attr('name'));
                }
        }
    }


    function addInlineValidation(){
    /* Inline Validation */
        $('input.blurrable, select.blurrable, textarea.blurrable').blur(function(){
            wrapper = $(this).parents("div[class*='kssattr-atfieldname']");
            serviceURL = $('base').attr('href') + '/' + '@@kssValidateField';
            params = {
                'fieldname': getKSSAttr(wrapper, 'atfieldname'),
                'value': $(this).val()
            };
            uid = getKSSAttr(wrapper, 'atuid');
            if (uid){
                params['uid'] = uid;
            }
            $.get(serviceURL, params, function(data){
                handleKSSResponse(data);
            });
        });
    }

    function addInlineEditing(){
        /* Inline Editing */
        $('.inlineEditable').click(function(){
            serviceURL = $('base').attr('href') + '/' + '@@replaceField';
            params = {
                'fieldname': getKSSAttr($(this), 'atfieldname'),
                'templateId': getKSSAttr($(this), 'templateId'),
                'macro': getKSSAttr($(this), 'macro'),
                'edit': 'True'
            };
            uid = getKSSAttr($(this), 'atuid');
            if (uid){
                params['uid']=uid;
            }
            target = getKSSAttr($(this), 'target');
            if (target){
                params['target']=target;
            }
            $.get(serviceURL, params, function(data){
                handleKSSResponse(data);
                registerInlineFormControlEvents();
            });
        });
    }

    function addCalendarChange(){
        /* Calendar update */
        $('a.kssCalendarChange').click(function(){
            serviceURL = $('base').attr('href') + '/' + '@@refreshCalendar';
            params = {
                'portlethash': getKSSAttr($(this), 'portlethash'),
                'year': getKSSAttr($(this), 'year'),
                'month': getKSSAttr($(this), 'month')
            };
            
            $.get(serviceURL, params, function(data){
                handleKSSResponse(data);
                addCalendarChange();
            });
            return false;
        });
    }

    function registerInlineFormControlEvents(){
        $('form.inlineForm input[name="kss-save"]').click(function(){
            serviceURL = $('base').attr('href') + '/' + '@@saveField';
            fieldname = getKSSAttr($(this), 'atfieldname');
            params = {
                'fieldname': fieldname
            };
        
            valueSelector = "input[name='" + params['fieldname'] + "']";
            value = $(this).parents('form').find(valueSelector).val();
            if (value){
                params['value']={
                    fieldname: value
                }
            }
        
            templateId = getKSSAttr($(this), 'templateId');
            if (templateId){
                params['templateId']=templateId;
            }
        
            macro = getKSSAttr($(this), 'macro');
            if (macro){
                params['macro']=macro;
            }
        
            uid = getKSSAttr($(this), 'atuid');
            if (uid){
                params['uid']=uid;
            }
        
            target = getKSSAttr($(this), 'target');
            if (target){
                params['target']=target;
            }

            $.get(serviceURL, params, function(data){
                handleKSSResponse(data);
            });        
        });
        
        $('form.inlineForm input[name="kss-cancel"]').click(function(){
            cancelInlineEdit(this);
        });
        
        $('input.blurrable, select.blurrable, textarea.blurrable').keypress(function(event){
            if (event.keyCode == 27){
                cancelInlineEdit(this);
            }
        });
    }

    function cancelInlineEdit(obj){
        serviceURL = $('base').attr('href') + '/' + '@@replaceWithView';
        fieldname = getKSSAttr($(obj), 'atfieldname');
        params = {'fieldname': fieldname,
                  'edit':      true};
        templateId = getKSSAttr($(obj), 'templateId');
        if (templateId){
            params['templateId']=templateId;
        }
    
        macro = getKSSAttr($(obj), 'macro');
        if (macro){
            params['macro']=macro;
        }
    
        uid = getKSSAttr($(obj), 'atuid');
        if (uid){
            params['uid']=uid;
        }
    
        target = getKSSAttr($(obj), 'target');
        if (target){
            params['target']=target;
        }
        $.get(serviceURL, params, function(data){handleKSSResponse(data);});
    }

})(jQuery);