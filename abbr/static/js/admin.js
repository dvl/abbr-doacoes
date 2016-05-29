django.jQuery(document).ready(function() {
  var fields = django.jQuery('.field-resposta_gateway p, .field-notificacao_gateway p');

  fields.each(function(i, block) {
    hljs.highlightBlock(block);
  });
});
