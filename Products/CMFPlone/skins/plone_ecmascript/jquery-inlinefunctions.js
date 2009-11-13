
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
    if(inherited.length){
        return getKSSAttr(inherited, varname);
    }
    else{
        return '';
    }
}

function handleKSSResponse(response){
    jQuery(response).find('command').each(
        function(){
            doKSSCommand(this);
        });
}

function extractSelector(command){
    selector = jQuery(command).attr('selector');
    selectorType = jQuery(command).attr('selectorType');
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
    switch(jQuery(command).attr('name')){
        case 'clearChildNodes':
            jQuery(selector).empty();
            break;
        case 'focus':
            jQuery(selector).focus();
            break;            
        case 'replaceHTML':
            html = jQuery(command).find('param[name="html"]').text();
            jQuery(selector).replaceWith(html);
            break;
        case 'replaceInnerHTML':
            html = jQuery(command).find('param[name="html"]').text();
            jQuery(selector).html(html);
            break;
        case 'setAttribute':
            attributeName = jQuery(command).find('param[name="name"]').text();
            replaceText = jQuery(command).find('param[name="value"]').text();
            jQuery(selector).attr(attributeName, replaceText);   
            break;
        case 'setStyle':
            name = jQuery(command).find('param[name="name"]').text();
            value = jQuery(command).find('param[name="value"]').text();
            jQuery(selector).css(name, value);
            break;
        default:
            console.log('No handler for command ' + jQuery(command).attr('name'));
    }
}

jQuery(function(){
    /* Inline Validation */
    jQuery('input.blurrable, select.blurrable, textarea.blurrable').blur(function(){
        wrapper = jQuery(this).parents("div[class*='kssattr-atfieldname']");
        serviceURL = jQuery('base').attr('href') + '/' + '@@kssValidateField';
        params = {'fieldname':   getKSSAttr(wrapper, 'atfieldname'),
                  'value':       jQuery(this).val()};
        uid = getKSSAttr(wrapper, 'atuid');
        if (uid){
            params['uid'] = uid;
        }
        jQuery.get(serviceURL, params, function(data){handleKSSResponse(data);});
    });
    
    /* Inline Editing */
    jQuery('.inlineEditable').click(function(){
        serviceURL = jQuery('base').attr('href') + '/' + '@@replaceField';
        params = {'fieldname':   getKSSAttr(jQuery(this), 'atfieldname'),
                  'templateId':  getKSSAttr(jQuery(this), 'templateId'),
                  'macro':       getKSSAttr(jQuery(this), 'macro'),
                  'edit':        'True'};
        uid = getKSSAttr(jQuery(this), 'atuid');
        if (uid){
            params['uid']=uid;
        }
        target = getKSSAttr(jQuery(this), 'target');
        if (target){
            params['target']=target;
        }
        jQuery.get(serviceURL, params,
            function(data){
                handleKSSResponse(data);
                registerInlineFormControlEvents();
            });
    });
});

function registerInlineFormControlEvents(){
    jQuery('form.inlineForm input[name="kss-save"]').click(function(){
        console.log('Inline save');
        
        serviceURL = jQuery('base').attr('href') + '/' + '@@saveField';
        fieldname = getKSSAttr(jQuery(this), 'atfieldname');
        params = {'fieldname': fieldname};
        
        valueSelector = "input[name='" + params['fieldname'] + "']";
        value = jQuery(this).parents('form').find(valueSelector).val();
        if (value){params['value']={fieldname: value}};
        
        templateId = getKSSAttr(jQuery(this), 'templateId');
        if (templateId){params['templateId']=templateId;}
        
        macro = getKSSAttr(jQuery(this), 'macro');
        if (macro){params['macro']=macro;}
        
        uid = getKSSAttr(jQuery(this), 'atuid');
        if (uid){params['uid']=uid;}
        
        target = getKSSAttr(jQuery(this), 'target');
        if (target){params['target']=target;}

        jQuery.get(serviceURL, params, function(data){handleKSSResponse(data);});        
    });
    jQuery('form.inlineForm input[name="kss-cancel"]').click(function(){
        cancelInlineEdit(this);
    });
    jQuery('form.inlineForm input[name="kss-cancel"]').click(function(){
        cancelInlineEdit(this);
    });
    jQuery('input.blurrable, select.blurrable, textarea.blurrable').keypress(function(event){
        if (event.keyCode == 27){cancelInlineEdit(this);}
    });
}

function cancelInlineEdit(obj){
    serviceURL = jQuery('base').attr('href') + '/' + '@@replaceWithView';
    fieldname = getKSSAttr(jQuery(obj), 'atfieldname');
    params = {'fieldname': fieldname,
              'edit':      true};
    templateId = getKSSAttr(jQuery(obj), 'templateId');
    if (templateId){params['templateId']=templateId;}
    
    macro = getKSSAttr(jQuery(obj), 'macro');
    if (macro){params['macro']=macro;}
    
    uid = getKSSAttr(jQuery(obj), 'atuid');
    if (uid){params['uid']=uid;}
    
    target = getKSSAttr(jQuery(obj), 'target');
    if (target){params['target']=target;}
    console.log(params);
    jQuery.get(serviceURL, params, function(data){handleKSSResponse(data);});
}

// Possible responses:
// 
// <!-- xmlns="http://www.kukit.org/commands/1.1" removed from kukit tag as it
//      breaks IE6 XP SP3 -->
// <commands>
// <command selector="div#archetypes-fieldname-title div.fieldErrorBox" name="clearChildNodes" selectorType="css">
// </command>
// <command selector="archetypes-fieldname-title" name="setAttribute" selectorType="htmlid">
//     <param name="name">class</param>
//     <param name="value">field Archetypestitlefield  kssattr-atfieldname-title</param>
// </command>
// </commands


// <commands>
// <command selector="div#archetypes-fieldname-title div.fieldErrorBox" name="replaceInnerHTML" selectorType="css">
//     <param name="html"><![CDATA[Title is required, please correct.]]></param>
//     <param name="withKssSetup">True</param>
// </command>
// <command selector="archetypes-fieldname-title" name="setAttribute" selectorType="htmlid">
//     <param name="name">class</param>
//     <param name="value">field error Archetypestitlefield  kssattr-atfieldname-title</param>
// </command>
// </commands>
// </kukit>

// <commands>
// <command selector=".portalMessage" name="setStyle" selectorType="css">
//     <param name="name">display</param>
//     <param name="value">none</param>
// </command>
// <command selector="kssPortalMessage" name="replaceInnerHTML" selectorType="htmlid">
//     <param name="html"><![CDATA[<dt>Info</dt><dd></dd>]]></param>
//     <param name="withKssSetup">True</param>
// </command>
// <command selector="kssPortalMessage" name="setAttribute" selectorType="htmlid">
//     <param name="name">class</param>
//     <param name="value">portalMessage info</param>
// </command>
// <command selector="kssPortalMessage" name="setStyle" selectorType="htmlid">
//     <param name="name">display</param>
//     <param name="value">none</param>
// </command>
// <command selector="parent-fieldname-title" name="replaceHTML" selectorType="htmlid">
//     <param name="html"><![CDATA[<span class=" kssattr-atfieldname-title kssattr-templateId-widgets/string kssattr-macro-string-field-view" id="parent-fieldname-title">
// <form class="field inlineForm enableUnloadProtection enableUnlockProtection" id="kss-inlineform-title">
// <div class="field ArchetypesStringWidget  kssattr-atfieldname-title" id="archetypes-fieldname-title">
// <span></span>
// <label class="formQuestion" for="title">Title</label>
// <span class="fieldRequired" title="Required">
//             (Required)
//           </span>
// <div class="formHelp" id="title_help"></div>
// <div class="fieldErrorBox"></div>
// <input type="text" name="title" class="blurrable firstToFocus" id="title" value="Test Page" size="30" maxlength="255" />
// </div>
// <div class="formControls">
// <input name="kss-save" value="Save" type="button" class="context" />
// <input name="kss-cancel" value="Cancel" type="button" class="standalone" />
// </div>
// </form>
// </span>]]></param>
//     <param name="withKssSetup">True</param>
// </command>
// <command selector="#parent-fieldname-title .firstToFocus" name="focus" selectorType="">
// </command>
// </commands>
