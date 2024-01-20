const DocumentModel = {
  inputId: '#document',
  balanceId: '#balance',
  nameId: '#name',
  successDiv: '#success-div',
  errorDiv: '#error-div',
  internalErrorDiv: '#internal-error',
  internalSuccessDiv: '#internal-success',
  btnSubmit: '#btn-submit',

  initializeListeners(){
    $(this.inputId).on('change', function(){
      let document = $(this).val()
      if(document.length == 11){
        DocumentModel.searchForBankAccount(document)
      }
    })
  },
  searchForBankAccount(document){
    $.get(`bankAccount/${document}`, this.showSuccess)
      .fail(this.showError)
  },
  showSuccess(data){
    $(DocumentModel.balanceId).text(data.balance)
    $(DocumentModel.nameId).text(data.name)
    $(DocumentModel.successDiv).show()
    $(DocumentModel.errorDiv).hide()
    $(DocumentModel.btnSubmit).attr('disabled', null)
    $(DocumentModel.internalErrorDiv).hide()
    $(DocumentModel.internalSuccessDiv).hide()
  },
  showError(){
    $(DocumentModel.errorDiv).show()
    $(DocumentModel.successDiv).hide()
    $(DocumentModel.btnSubmit).attr('disabled', true)
    $(DocumentModel.internalErrorDiv).hide()
    $(DocumentModel.internalSuccessDiv).hide()
  },
}

$(function() {
  DocumentModel.initializeListeners()
});