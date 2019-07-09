var grid = $("#grid-medic").bootgrid({
  ajax: true,
  rowSelect: true,
  labels:{
    infos: "Affichage de l'élément {{ctx.start}} à {{ctx.end}} sur un total de {{ctx.total}} éléments",
    search: "Recherche"
  },

  post: function ()
  {
    /* To accumulate custom parameter with the request object */
    return {
      id: "b0df282a-0d67-40e5-8558-c9e93b7befed"
    };
  },

  url: "/loadMedic",

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
      $('#edit_libmedic').val(ele.siblings(':nth-of-type(2)').html());
      $('#edit_descmedic').val(ele.siblings(':nth-of-type(3)').html());
    } else {
      alert('First select row, then click edit button');
    }
  }).end().find(".command-delete").on("click", function(e){
    var conf = confirm("Voulez vous supprimer l'item n° " + $(this).data("row-id") );
    if(conf){
      $(this).parent().parent().remove();
      $("#grid-retailer").bootgrid('remove', $(this).data("row-id"))
      $.ajax({
        url:'/deleteMedic',
        type:'DELETE',
        data: 'id=' + $(this).data("row-id"),
      })  
    }
  });
});

$( "#btn_edit" ).click(function(){
  $.ajax({
    url:'/editMedic',
    type:'PUT',
    data: $('#frm_edit').serialize(),
  })

  grid.bootgrid("reload")

});


