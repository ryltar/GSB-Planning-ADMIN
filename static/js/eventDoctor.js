var grid = $("#grid-doctor").bootgrid({
  labels:{
    infos: "Affichage de l'élément {{ctx.start}} à {{ctx.end}} sur un total de {{ctx.total}} éléments",
    search: "Recherche"
  },
  ajax: true,
  rowSelect: true,
  sorting: true,

  post: function ()
  {
    /* To accumulate custom parameter with the request object */
    return {
      id: "b0df282a-0d67-40e5-8558-c9e93b7befed"
    };
  },

  url: "/loadDoctor",

  formatters: {
    "commands": function(column, row)
    {
      return "<button type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\"><span class=\"fa fa-pencil\"></span></button> " +
      "<button type=\"button\" class=\"btn btn-xs btn-default command-delete\" data-row-id=\"" + row.id + "\"><span class=\"fa fa-trash-o\"></span></button>";
    }
  }

}).on("loaded.rs.jquery.bootgrid", function()
{
  grid.find(".command-edit").on("click", function(e)
  {
    
    
    var ele =$(this).parent();
    if($(this).data("row-id") > 0) {
      $('#edit_model').modal('show');
      $('#edit_id').val(ele.siblings(':first').html());
    
      $('#edit_lastname').val(ele.siblings(':nth-of-type(2)').html());
      $('#edit_firstname').val(ele.siblings(':nth-of-type(3)').html());
      $('#edit_email').val(ele.siblings(':nth-of-type(4)').html());
      $('#edit_num').val(ele.siblings(':nth-of-type(5)').html());

      for(i = 0; i<$('#edit_employee option').length; i++ ){
        if ($('#edit_employee option')[i].value == ele.siblings(':nth-of-type(6)').html().toString()){
          $('#edit_employee option')[i].selected = true
        }

      }

      for(i = 0; i<$('#edit_address option').length; i++ ){
        if ($('#edit_address option')[i].value == ele.siblings(':nth-of-type(7)').html().toString()){
          $('#edit_address option')[i].selected = true
        }

      }

      for(i = 0; i<$('#edit_specialty option').length; i++ ){
        if ($('#edit_specialty option')[i].value == ele.siblings(':nth-of-type(8)').html().toString()){
          $('#edit_specialty option')[i].selected = true
        }

      }

    } else {
      alert('First select row, then click edit button');
    }
  }).end().find(".command-delete").on("click", function(e){
    var conf = confirm("Voulez vous supprimer l'item n° " + $(this).data("row-id") );
    if(conf){
      $(this).parent().parent().remove();
      $("#grid-employee").bootgrid('remove', $(this).data("row-id"))
      $.ajax({
        url:'/deleteDoctor',
        type:'DELETE',
        data: 'id=' + $(this).data("row-id"),
      })  
    }
  })
});

$( "#btn_edit" ).click(function(){
  $.ajax({
    url:'/editDoctor',
    type:'PUT',
    data: $('#frm_edit').serialize(),
  })

  grid.bootgrid("reload")

});



