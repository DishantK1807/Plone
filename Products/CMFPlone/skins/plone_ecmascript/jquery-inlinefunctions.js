
function getKSSAttr(obj, varname){
    classes = obj.attr('class').split(' ');
    classname = 'kssattr-' + varname + '-';
    for (i in classes){
        cls = classes[i];
        if(cls.indexOf(classname) >= 0){
            return cls.substring(classname.length, cls.length);
        }
    }
    return '';
}

function handleKSSResponse(response){
    clearCommand = jQuery(response).find('command[name="clearChildNodes"]');
    if (clearCommand.length > 0){
        selector = jQuery(clearCommand).attr('selector');
        jQuery(selector).empty();
    }
    setAttributeCommand = jQuery(response).find('command[name="setAttribute"]');
    if (setAttributeCommand.length > 0){
        selector = jQuery(setAttributeCommand).attr('selector');
        attributeName = jQuery(setAttributeCommand).find('param[name="name"]').text();
        replaceText = jQuery(setAttributeCommand).find('param[name="value"]').text();
        jQuery('#' + selector).attr(attributeName, replaceText);
    }
    replaceInnerHTMLCommand = jQuery(response).find('command[name="replaceInnerHTML"]');
    if (replaceInnerHTMLCommand.length > 0){
        selector = jQuery(replaceInnerHTMLCommand).attr('selector');
        replaceHTML = jQuery(replaceInnerHTMLCommand).find('param[name="html"]').text();
        jQuery(selector).html(replaceHTML);
    }

}

/* Inline Validation */
jQuery(function(){
    jQuery('input.blurrable, select.blurrable, textarea.blurrable').blur(function(){
        value = jQuery(this).val();
        wrapperdiv = jQuery(this).parents("div[class*='kssattr-atfieldname']");
        fieldname = getKSSAttr(wrapperdiv, 'atfieldname');
        uid = getKSSAttr(wrapperdiv, 'atuid');
        serviceURL = jQuery('base').attr('href') + '/' + '@@kssValidateField';
        jQuery.get(serviceURL, {'fieldname': fieldname, 'value': value, 'uid': uid}, handleKSSResponse(data));
    });

});



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
